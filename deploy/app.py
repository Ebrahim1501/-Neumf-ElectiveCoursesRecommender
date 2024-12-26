import flask
import pandas as pd
from flask import Flask, render_template, session, redirect, url_for, request
from utils import get_topk_recommendations,deserialize_object
import tensorflow as tf
import keras
import pickle
import requests
from google.api_core.exceptions import GoogleAPICallError 
import google.generativeai as genai

#file containing my personal api keys...
import credentials


gemini=genai.GenerativeModel("gemini-1.5-pro")


GOOGLE_API_KEY=my_key


genai.configure(api_key=GOOGLE_API_KEY)





#Loading gemini responses!!!def get_gemini_responses(course_names_list, k=5):
def get_gemini_responses(course_names_list, k=5):
    responses = []
    for i in range(k):
        message = f"Write a brief description about the course called {course_names_list[i][1]}"
        try:
            response = gemini.generate_content(message)
            if hasattr(response, 'error') and response.error:
                responses.append("Description not available due to API error")
            else:
                description = response.text  # Adjust this according to the Gemini API response structure
                responses.append(description)
        except GoogleAPICallError as e:
            print(f"Google API call error: {e}")
            responses.append("Description not available due to API error")
    
    return responses






# Function to encode student serial to student_id

def encode_serial(student_serial):

    encoded_serial = lookup_df.loc[lookup_df['student serial'].astype(str) == str(student_serial), 'student_id'].values #compare them as strings
    if len(encoded_serial) > 0:
        return encoded_serial[0]  # Assuming only one match expected
    else:
        return None

# Function to decode course_id to Course Name
def decode_course(course_id):
    decoded_course = lookup_df.loc[lookup_df['course_id'] == course_id, 'Course Name'].values
    if len(decoded_course) > 0:
        return decoded_course[0]  # Assuming only one match
    else:
        return None 
    
    
def not_taken_courses(student_num):
    # Filter courses taken by the student
    courses_taken = lookup_df.loc[lookup_df['student_id'] == student_num, 'course_id'].unique()

    # Get all unique courses
    all_courses = lookup_df['course_id'].unique()

    # Find courses not taken
    courses_not_taken = [course for course in all_courses if course not in courses_taken]

    return courses_not_taken







model=deserialize_object('D:\\GraduationProject\\myneumf-trained-model.pkl')
#model = keras.models.load_model('model.keras')

lookup_df = pd.read_csv('D:\\GraduationProject\\lookuptable.csv')



app = Flask(__name__)

app.secret_key = my_key  # Set a secret key for session management

# Route for the index page (login form)
@app.route('/')
def index():
    return flask.render_template('login.html')

# Route to handle login form submission
@app.route('/login', methods=['POST'])
def login():
    if flask.request.method == 'POST':
        student_name = flask.request.form['studentName'].strip()
        student_number = flask.request.form['studentNumber'].strip()
        #print(f"Student Name: {student_name}, Student Number: {student_number}")

        # Validate student number against lookup table
        if student_number in lookup_df['student serial'].astype(str).values:
            # Store student details in session
            session['student_name'] = student_name
            session['student_number'] = student_number
            
            print("Redirecting to recommendation page...")


            # Redirect to recommendation page (electivecourses.html)
            return flask.redirect(flask.url_for('recommendation'))
        else:
            error_message = 'Student ID is not correct. Please use a valid one.'
            print("Student ID validation failed.")
            return flask.render_template('login.html', error_message=error_message)

@app.route('/recommendation')

@app.route('/recommendation')
def recommendation():
    if 'student_name' in session and 'student_number' in session:
        student_name = session['student_name']
        student_number = session['student_number']
        student_id = encode_serial(student_number)

        remaining_courses = not_taken_courses(student_id)
        recommendations = get_topk_recommendations(model=model, student_id=student_id, courses=remaining_courses, k=len(remaining_courses))
        # Decode course IDs back to their names
        recommendations = [(course_id, decode_course(course_id)) for course_id in recommendations]
        descs=get_gemini_responses(recommendations)
        print("description:",descs)

        print(f"Rendering recommendation page for {student_name} ({student_number})")
        return flask.render_template('electivecourses.html', student_name=student_name, student_number=student_number, recommendations=recommendations,descs=descs)
    else:
        print("Session data missing, redirecting to login page.")
        return flask.redirect(flask.url_for('index'))
    
    # Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
