# -Neumf-ElectiveCoursesRecommender


## NeuMf Based Elective Courses Recommender System
This project is my implementation of the architecture described in the[Neural Collaborative Filtering](https://arxiv.org/pdf/1708.05031)research paper,which is considered as one of the cutting edge technologies in the field of recommender systems. The goal of this project is to create an efficient and privacy-preserving elective courses recommender system.

The system only relies on the student’s performance history in previous courses to generate a list of top-k recommended subjects. These subjects are selected based on their high likelihood of improving the student’s academic performance. Importantly, the system does not require any prior knowledge about the student's personal information, ensuring that the student's data privacy is maintained.

The model uses the student’s history of final grades in various subjects as explicit feedback (ratings), which forms the basis for generating recommendations. By utilizing the Neural Collaborative Filtering (NeuMF) architecture, the system provides personalized, efficient, and data-driven recommendations to help students maximize their academic satisfaction and, more importantly, their performance.

---
## Workflow

1. **Collecting AAST Student Data**  
   Gather real-life student data from my AAST-University data center for the recommendation process.

2. **Data Cleaning and Preprocessing**  
   Perform necessary data cleaning and preprocessing tasks such as removing null values, outliers, data normalization, and augmentation.

3. **Training and Evaluating the Model**  
   Train the model and manually tune the hyperparameters to achieve the best results. Evaluate the model using popular recommender system evaluation metrics.

4. **Saving the Trained Model**  
   Save the trained model to a file for deployment.

5. **Developing a Simple Flask Web App**  
   Create a Flask web application to interact with the model and display recommendations in a user-friendly interface.

6. **Dockerizing the Application**  
   Containerize the Flask application using Docker for easier future deployment.

7. **Deploying the App to Heroku**  
   Deploy the Dockerized Flask app to Heroku for real-life usage.
---

## Project Recommendations Sample:



https://github.com/user-attachments/assets/5511b6ab-6943-43dd-ac38-ec61644ef56c






## Repo Content:

- **Neumf-ElectiveCoursesRecommender**  
    - `NeuMF-Recommender.ipynb`: Notebook used for model training and evaluation  
    - `utils.py`: Utility functions used by both the notebook and the Flask app

- **deploy**  
    - `app.py`: Flask back-end app  
    - `Dockerfile`: Used for building an image for the WebApp  
    - `lookuptable.csv`: An auxiliary table used by the model to map encoded course and student IDs to their actual IDs  
    - `myneumf-trained-model.pkl`: Saved model  
    - `requirements.txt`: Requirements for the Flask app  
    - `utils.py`: Utility functions used by both the notebook and the Flask app  

    - **templates**  
        - Contains all the CSS and HTML files used by the Flask app  


- **Images**  
    - Contains snapshots for evaluation curves, model architecture, and sample outputs

      ---

## Architecture Overview

### **Neural Collaborative Filtering (NeuMF)**
- **Input Layer**:
  - User Identifier (Student ID): Encoded as unique integers.
  - Item Identifier (Course ID): Encoded as unique integers.
- **Embedding Layers**:
  - User Embedding: Dense vector representation for users.
  - Item Embedding: Dense vector representation for items.
- **Matrix Factorization (MF)**:
  - Captures linear interactions relationships between users and courses.
  - Approximates user-course interaction matrix through latent factors using point-wise multiplication.
- **Multi-Layer Perceptron (MLP)**:
  - 3 hidden layers with neurons [128, 64, 32] and Relu activation function.
  - Used for capturing nonlinear interactions relationships between users and courses.
- **Concatenation Layer**:
  - Combines and concatenates outputs from MF and MLP components.
- **Output Layer**:
  - Predicts normalized interaction scores (0 to 1) using an output dense layer .


### **System Architecture Diagram**

![neumf-colored](https://github.com/user-attachments/assets/1c4bb064-e199-4da6-b5ae-090c681739c1)


![Architecture-of-Neural-Collaborative-Filtering](https://github.com/user-attachments/assets/ff9361a0-58d0-4dc7-bbf8-2e7316c3e59e)


---
## Performance Evaluation
- **Metrics Used**:
  - Training & Validation Losses
  - Hit Rate (HR)
  - Normalized Discounted Cumulative Gain (NDCG)
- **Results Of These Metrics Can Be Found [Here](https://github.com/Ebrahim1501/-Neumf-ElectiveCoursesRecommender/tree/main/Images)**:

---





## To Clone The Repository:
   ```bash
   git clone https://github.com/Ebrahim1501/-Neumf-ElectiveCoursesRecommender.git
   cd <your project directory here>
```
```bash
   pip install -r deploy/requirement.txt
```
## Run The  FlaskApp locally Using 
```bash
python deploy/app.py
```
## To Build&run The Flask's Docker Image
```bash
docker build -t elective-recommender .
docker run -p 5000:5000 elective-recommender
```

