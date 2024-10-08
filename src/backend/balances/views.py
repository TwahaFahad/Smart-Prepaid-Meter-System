from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from accounts.models import AccountMeter
from balances.models import ElectricityBalance, ElectrictyBalanceLog, Token

# Create your views here.

import random
import time
import threading
from django.http import JsonResponse



from .real import predict_and_detect_anomalies, predict_and_detect_anomalies2

real_time_data = {
    'actual_values': [],
    'predicted_values': [],
    'anomalies': [],
    'actual_values2': [],
    'predicted_values2': [],
    'anomalies2': [],
}



def generate_random_value():
    if random.random() < 0.8:
        return round(random.uniform(0, 55.5), 3) 
    else:
        return round(random.uniform(0, 55.5), 3) 
    
def generate_random_value2():
    if random.random() < 0.8:
        return round(random.uniform(0, 7.5), 3) 
    else:
        return round(random.uniform(0, 7.5), 3) 


def generate_values():
    global real_time_data
    while True:
        new_value = generate_random_value()
        new_value2 = generate_random_value2()
        
 
        predicted_value, is_spike, is_prolonged = predict_and_detect_anomalies(new_value)
        
        predicted_value2, is_spike2, is_prolonged2 = predict_and_detect_anomalies2(new_value2)

  
        new_value = round(float(new_value), 2)
        predicted_value = round(float(predicted_value), 2)
        new_value2 = round(float(new_value2), 2)
        predicted_value2 = round(float(predicted_value2), 2)

 
        real_time_data['actual_values'].append(new_value)
        real_time_data['predicted_values'].append(predicted_value)
        
        real_time_data['actual_values2'].append(new_value2)
        real_time_data['predicted_values2'].append(predicted_value2)
        
        if is_spike or is_spike2:
            real_time_data['anomalies'].append((new_value, "Sudden Spike"))
            real_time_data['anomalies2'].append((new_value2, "Sudden Spike"))
        elif is_prolonged or is_prolonged2:
            real_time_data['anomalies'].append((new_value, "Prolonged High"))
            real_time_data['anomalies2'].append((new_value2, "Prolonged High"))

        time.sleep(5) 


def start_background_task():
    thread = threading.Thread(target=generate_values)
    thread.daemon = True
    thread.start()

start_background_task()



def get_real_time_data(request):
    return JsonResponse(real_time_data)





@login_required(login_url='accounts:login')
def dashboardView(request):

    user = request.user

    meter_details = get_object_or_404(AccountMeter, account=user)

    current_balance = get_object_or_404(ElectricityBalance, meter_no=meter_details)
    
    context = {
        'current_balance': current_balance,
        'meter_details': meter_details
    }
    return render(request, 'balances/main-dashboard.html', context)


@login_required(login_url='accounts:login')
def tokenHistoryView(request):

    user = request.user

    meter_details = get_object_or_404(AccountMeter, account=user)

    token_history = Token.objects.filter(meter_no=meter_details)

    context = {
        'token_history': token_history
    }
    return render(request, 'balances/history.html', context)


def anomalyDashboard(request):
    
    context = {
        
    }
    return render(request, 'balances/anomaly.html', context)
