# -*- coding: utf-8 -*-
"""

Predict + Anomaly Detection
This code predicts household consumption values using an LSTM model and detects anomalies based on the prediction.
Anomalies are defined as either sudden spikes (large deviations) or prolonged higher consumption.

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Dropout

# Load dataset
df = pd.read_csv('household_consumption.csv')
# Drop any rows with missing values to ensure data integrity
df.dropna(inplace=True)

# Split the dataset into training and test sets
# The whole dataset is (34954, 2), consumption for every 30 min
# First 27,754 entries for training
training_set = df.iloc[:27754,1:2].values
# Remaining 7200 (10 days) entries for testing
test_set = df.iloc[27754:,1:2].values

# Feature scaling
# Normalizes the data to values between 0 and 1 to improve training performance of the LSTM
sc = MinMaxScaler(feature_range = (0,1))

# Apply scaling on both training and test sets
# Fit and transform training data
training_set_scaled = sc.fit_transform(training_set)
# Only transform test data (using the same scaling)
test_set_scaled = sc.fit_transform(test_set)



# Window size (ws) refers to how many previous time steps the model will look at to predict the next value
# Increasing ws means the model considers more past data points, which might improve long-term trend prediction but increases computational complexity.
# Decreasing ws reduces the data used by the model, potentially making predictions too short-sighted and noisy.
# The window size is set to 48 (representing 24 hours of data for 30-minute intervals)
ws = 48

# Prepare training data by creating sequences of 48 (ws) time steps to predict the next step
x_train = []  # To hold sequences of past consumption values
y_train = []  # To hold the target value (next consumption after the sequence)

# Create the input sequences and corresponding outputs
# Start from ws because the first sequence starts at index ws
for i in range(ws,len(training_set_scaled)):
    x_train.append(training_set_scaled[i-ws:i, 0:1]) # The sequence of the previous ws time steps
    y_train.append(training_set_scaled[i, 0]) # The value we're predicting (next step after the sequence)

# Convert lists into numpy arrays, so they can be fed into the neural network    
x_train, y_train = np.array(x_train), np.array(y_train)



"""
Build the model
"""

# Initialize an LSTM-based Sequential model
Model_Pred = Sequential()

# First LSTM layer with 60 units, return_sequences=True means the output will be passed to the next LSTM layer
# The input_shape (ws,1) means that the model will accept sequences of length 'ws' and one feature (consumption).
# units=60 specifies the number of LSTM units (neurons) in this layer.
Model_Pred.add(LSTM(units = 60, return_sequences = True, input_shape = (x_train.shape[1],1)))
# Dropout regularization to prevent overfitting, drops 20% of neurons randomly during training
Model_Pred.add(Dropout(0.2))

# Second LSTM layer, also returning sequences to allow stacking of LSTM layers
Model_Pred.add(LSTM(units = 60, return_sequences = True))
Model_Pred.add(Dropout(0.2))

# Third LSTM layer, still returning sequences for further learning of temporal patterns
Model_Pred.add(LSTM(units = 60, return_sequences = True))
Model_Pred.add(Dropout(0.2))

# Fourth LSTM layer, but return_sequences=False, meaning this is the last LSTM layer
Model_Pred.add(LSTM(units = 60))
Model_Pred.add(Dropout(0.2))

# Dense output layer with 1 neuron to predict the next consumption value
Model_Pred.add(Dense(units = 1))

# Compile the model with 'adam' optimizer and mean squared error loss function
Model_Pred.compile(optimizer = 'adam', loss = 'mean_squared_error')

# Train the model using the prepared training data
# Epochs is the number of complete passes through the training dataset.
# Batch_size is the number of samples processed before the model is updated.
# Increasing epochs might improve accuracy but leads to overfitting if too high.
# Batch_size affects the stability and speed of training. A larger batch size might stabilize updates but requires more memory.
Model_Pred.fit(x_train, y_train, epochs = 30, batch_size = 32)

"""
Saving the trained model
"""
# you can use any name, here i used fypred, but any name can work
Model_Pred.save('fypred')

"""
Load the saved model for predictions
"""
#If you want to load the model and use it, this is the code.
#here, i didn't load the model, i just wanted to show you the code, since you can not be running the codes above everytime.
from keras.models import load_model
Model_Pred = load_model('fypred')

"""
Plot the training loss over epochs to observe how well the model converges
"""
# you can see how the error is changing and you can choose to change the epochs number
plt.plot(range(len(Model_Pred.history.history['loss'])),Model_Pred.history.history['loss'])
plt.xlabel('Epoch Number')
plt.ylabel('Loss')
plt.show()



# Function to detect anomalies
def detect_anomalies(input_values, threshold=1.5, prolonged_threshold=6):
    """
    Detect anomalies based on sudden spikes and prolonged higher consumption.
    threshold(float): Adjusts how sensitive the model is to spikes (increase to make the model less sensitive).
    prolonged_threshold(int): Number of consecutive higher values before classifying as prolonged anomaly.
    input_values (list/array): Actual consumption values to check for anomalies.
    """
    # Scale the input values
    input_scaled = sc.transform(np.array(input_values).reshape(-1, 1))
    
    # Prepare input batch (sliding window)
    batch_new = training_set_scaled[-ws:].reshape((1, ws, 1)) # Start with last window of training data
    prediction_test = []
    
    for val in input_scaled:
        pred = Model_Pred.predict(batch_new)[0]
        prediction_test.append(pred)
        
        # Update the batch for the next prediction
        batch_new = np.append(batch_new[:,1:,:], [[val]], axis = 1)
    
    predictions = sc.inverse_transform(np.array(prediction_test).reshape(-1, 1)) # Predicted values
    
    # Detect anomalies based on threshold
    anomalies = []
    consecutive_high_count = 0
    
    for i in range(len(input_values)):
        actual_value = input_values[i]
        predicted_value = predictions[i][0]
        
        # Check for sudden spike (actual value > predicted + threshold)
        if actual_value > (predicted_value * (1 + threshold)):
            anomalies.append((i, actual_value, 'Sudden Spike'))
        
        # Check for prolonged high consumption
        if actual_value > predicted_value:
            consecutive_high_count += 1
            if consecutive_high_count >= prolonged_threshold:
                anomalies.append((i, actual_value, 'Prolonged High Consumption'))
        else:
            consecutive_high_count = 0
    
    return predictions, anomalies




test_df = pd.DataFrame(test_set)
test_df.to_csv('test_set.csv', index=False)

testing_sec = pd.read_csv('test_set.csv')
df.dropna(inplace=True)


testing_sec_array = testing_sec.to_numpy()

# Example Usage: Detect anomalies in the first 96 values of the test set
# for the Input values, i've used here are the data from the test_set,
# you can use any number value(s) and test t.
# remember its an array/list.
#the input values here are from index 0 to 96.
# my predictions values were also 96.
#make sure to compare the actual values with similar predicted values
input_values = testing_sec_array[:96].flatten()  # Input values (e.g., 96 consecutive values)
predictions, anomalies = detect_anomalies(input_values)


# Plot predictions vs actual values
plt.plot(input_values, color='red', label='Actual Values')
plt.plot(predictions, color='blue', label='Predicted Values')
plt.title('LSTM - Prediction vs Actual')
plt.xlabel('Time')
plt.ylabel('Consumption')
plt.legend()
plt.show()

# Print out the detected anomalies
if anomalies:
    print("Detected anomalies:")
    for anomaly in anomalies:
        print(f"Index: {anomaly[0]}, Value: {anomaly[1]}, Type: {anomaly[2]}")
else:
    print("No anomalies detected.")





