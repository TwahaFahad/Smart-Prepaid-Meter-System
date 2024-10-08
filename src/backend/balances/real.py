# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 09:55:29 2024

@author: RSL T14 001
"""

# Load trained LSTM model
import os
from keras.models import load_model
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


# Get the directory of the current file (real.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the ml_models folder
ml_models_path = os.path.join(current_dir, '..', 'models')

# Construct the path to the fypred folder within ml_models
model_path = os.path.join(ml_models_path, 'pcpred')

# Construct the path to the fypred folder within ml_models
model_path2 = os.path.join(ml_models_path, 'bulbpred')

# Load the trained LSTM model
Model_Pred = load_model(model_path)

Model_Pred2 = load_model(model_path2)

# Assume we have a new value coming in every 30 minutes
# For this example, we'll simulate the incoming data as the first 100 values of the test set

csv_path = os.path.join(ml_models_path, 'PC_dataset.csv')
# Set up the scaler
df = pd.read_csv(csv_path)
sc = MinMaxScaler(feature_range=(0, 1))
training_set = df.iloc[:27754,1:2].values
training_set_scaled = sc.fit_transform(training_set)


csv_path2 = os.path.join(ml_models_path, 'Bulb_dataset.csv')
# Set up the scaler
df2 = pd.read_csv(csv_path2)
training_set2 = df2.iloc[:27754,1:2].values
training_set_scaled2 = sc.fit_transform(training_set2)





# Rolling window size (ws)
ws = 48

# Prepare the initial window (last 48 values from training set)
rolling_window = training_set_scaled[-ws:].reshape((1, ws, 1))  # 3D array for LSTM

rolling_window2 = training_set_scaled2[-ws:].reshape((1, ws, 1)) 

# Global variable to track consecutive high counts
consecutive_high_count = 0

def predict_and_detect_anomalies(new_value, threshold=1.5, prolonged_threshold=6):
    global rolling_window, consecutive_high_count
    
    # Scale the new value (since your model was trained on scaled data)
    new_value_scaled = sc.transform(np.array([[new_value]]))
    
    # Predict the next value based on the current window
    predicted_value_scaled = Model_Pred.predict(rolling_window)[0][0]
    predicted_value = sc.inverse_transform(np.array([[predicted_value_scaled]]))[0][0]  # Unscale prediction
    
    # Initialize anomaly flags
    is_spike = False
    is_prolonged = False
    
    # Detect anomalies
    # 1. Sudden Spike (actual value > predicted * (1 + threshold))
    if new_value > (predicted_value + 2) * (1 + threshold):
        print(f"Sudden Spike Detected: Actual={new_value}, Predicted={predicted_value}")
        is_spike = True
    
    # 2. Prolonged High Consumption (actual > predicted for prolonged_threshold consecutive times)
    if new_value >= (predicted_value + 0.01):
        consecutive_high_count += 1
        if consecutive_high_count >= prolonged_threshold:
            print(f"Prolonged High Consumption Detected: Actual={new_value}, Predicted={predicted_value}")
            is_prolonged = True
    else:
        # Reset the counter if the actual value goes below the predicted
        consecutive_high_count = 0
    
    # Update the rolling window by dropping the oldest value and appending the new one
    new_value_scaled = np.reshape(new_value_scaled, (1, 1, 1))  # Reshape to (1, 1, 1)
    rolling_window = np.append(rolling_window[:, 1:, :], new_value_scaled, axis=1)
    
    return predicted_value, is_spike, is_prolonged  # Return all three values

# Simulate receiving new data and detect anomalies
#test_set = df.iloc[27754:, 1:2].values   Test data (after the training set)


# testing_sec = pd.read_csv('test_set.csv')
# test_set = testing_sec.to_numpy()
# for new_value in test_set[:100]:  # Assume we're processing the first 100 new values
#     predict_and_detect_anomalies(new_value[0])

def predict_and_detect_anomalies2(new_value2, threshold=1.5, prolonged_threshold=6):
    global rolling_window2, consecutive_high_count
    
    # Scale the new value (since your model was trained on scaled data)
    new_value_scaled = sc.transform(np.array([[new_value2]]))
    
    # Predict the next value based on the current window
    predicted_value_scaled = Model_Pred.predict(rolling_window2)[0][0]
    predicted_value2 = sc.inverse_transform(np.array([[predicted_value_scaled]]))[0][0]  # Unscale prediction
    
    # Initialize anomaly flags
    is_spike2 = False
    is_prolonged2 = False
    
    # Detect anomalies
    # 1. Sudden Spike (actual value > predicted * (1 + threshold))
    if new_value2 > (predicted_value2 + 2) * (1 + threshold):
        print(f"Sudden Spike Detected: Actual={new_value2}, Predicted={predicted_value2}")
        is_spike2 = True
    
    # 2. Prolonged High Consumption (actual > predicted for prolonged_threshold consecutive times)
    if new_value2 >= (predicted_value2 + 0.01):
        consecutive_high_count += 1
        if consecutive_high_count >= prolonged_threshold:
            print(f"Prolonged High Consumption Detected: Actual={new_value2}, Predicted={predicted_value2}")
            is_prolonged2 = True
    else:
        # Reset the counter if the actual value goes below the predicted
        consecutive_high_count = 0
    
    # Update the rolling window by dropping the oldest value and appending the new one
    new_value_scaled = np.reshape(new_value_scaled, (1, 1, 1))  # Reshape to (1, 1, 1)
    rolling_window2 = np.append(rolling_window2[:, 1:, :], new_value_scaled, axis=1)
    
    return predicted_value2, is_spike2, is_prolonged2  # Return all three values



