# -*- coding: utf-8 -*-
"""Utils.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/119smSG0zRjnnJ3b3JNyc6eKBHnh-Tzf_

Libraries
"""

import pickle
import numpy as np
import pandas as pd



def augment_data(dataset: pd.DataFrame, target_col: str, threshold: float, duplication_factor=1) -> pd.DataFrame:
  """
  Augments a dataset by duplicating rows with target values below a threshold
  and adding random noise to the target column.

  Args:
      dataset (pd.DataFrame): The dataset to be augmented.

      target_col (str): The name of the column containing the target variable.

      threshold (float): The threshold value for target variable duplication.
          Rows with target values less than or equal to the threshold are duplicated.

      duplication_factor (int, optional): The number of times to duplicate rows
          that meet the threshold criteria. Defaults to 1 (duplicate once).

  Returns:
      pd.DataFrame: The augmented dataset containing both original and duplicated rows.
  """

  augmented_rows = []

  for index, row in dataset.iterrows():
    # Check if target value meets duplication criteria
    if row[target_col] <= threshold:
      for _ in range(duplication_factor):
        # Generate random noise within a selected range 
        noise = np.random.uniform(low=-1, high=1)
        augmented_value = row[target_col] + noise

        # Create a new row with augmented target value
        augmented_row = {}
        for col in dataset.columns:
          augmented_row[col] = row[col] if col != target_col else augmented_value
        augmented_rows.append(augmented_row)
    else:
      # Add original row if it doesn't qualify for augmentation
      augmented_rows.append(row.to_dict())

  # Concatenate original dataset with augmented rows
  augmented_dataset = pd.DataFrame(augmented_rows)

  return augmented_dataset






def serialize(obj, filename):
  """Serializes a Python object to a file using pickle.

  Args:
    obj: The Python object to serialize.
    filename: The name of the file to save the serialized object to.
  """



  with open(filename, 'wb') as file:
    pickle.dump(obj, file)




def deserialize_object(filename):
  """Deserializes a Python object from a file using pickle.

  Args:
    filename: The name of the file containing the serialized object.

  Returns:
    The deserialized Python object.
  """

  with open(filename, 'rb') as file:
    return pickle.load(file)





def get_topk_recommendations(model, student_id, courses, k=5):
    """Get Top k recommendations based on student_id.

    Args:
    model: pre-trained recommendation model.
    student_id: the encoded id for the desired student.
    courses: list of courses encoded ID's.
    k: number of top Recommended objects.

    Returns:
    List of course IDs recommended for the student.
    """

    student_input = np.array([student_id])
    student_input = np.repeat(student_input, len(courses))
    course_inputs = np.array(courses)

    predictions = model.predict([student_input, course_inputs])
    predictions = predictions.flatten()

    predictions_df = pd.DataFrame({'course_id': courses, 'prediction': predictions})

    topk = predictions_df.nlargest(k, 'prediction')  # Get top k recommendations

    return topk['course_id']
