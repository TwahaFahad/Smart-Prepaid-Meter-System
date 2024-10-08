
import random
import time
import threading
from django.http import JsonResponse
from django.shortcuts import render
from django.http import JsonResponse


#from .real import predict_and_detect_anomalies

# Now you can import real.py from the packages folder
from real import predict_and_detect_anomalies

# Store real-time data for the dashboard
real_time_data = {
    'actual_values': [],
    'predicted_values': [],
    'anomalies': [],
}

# Function to generate random values between 0 and 4 (with more lower values)
def generate_random_value():
    if random.random() < 0.8:
        return round(random.uniform(0.000, 2.000), 3)  # More frequent values
    else:
        return round(random.uniform(2.000, 4.000), 3)  # Less frequent values

# Function to continuously generate random values and update the dataset
def generate_values():
    global real_time_data
    while True:
        new_value = generate_random_value()
        
        # You can call your prediction and anomaly detection here
        predicted_value, is_spike, is_prolonged = predict_and_detect_anomalies(new_value)

        # Convert numpy.float32 to Python float to ensure JSON serialization works
        new_value = float(new_value)
        predicted_value = float(predicted_value)

        # Update real-time data
        real_time_data['actual_values'].append(new_value)
        real_time_data['predicted_values'].append(predicted_value)
        
        if is_spike:
            real_time_data['anomalies'].append((new_value, "Sudden Spike"))
        elif is_prolonged:
            real_time_data['anomalies'].append((new_value, "Prolonged High"))

        time.sleep(5)  # Simulating 30-minute intervals with 5 seconds delay

# Start the background thread to generate values
def start_background_task():
    thread = threading.Thread(target=generate_values)
    thread.daemon = True
    thread.start()

start_background_task()


# View to return the latest data
def get_real_time_data(request):
    return JsonResponse(real_time_data)

def dashboard(request):
    return render(request, 'dashboard.html')