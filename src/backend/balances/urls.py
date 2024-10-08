from django.urls import path

from . import views

app_name = 'balances'


urlpatterns = [
    path('', views.dashboardView, name='dashboard'),
    path('token-history/', views.tokenHistoryView, name='token-history'),
    path('anomaly-dashboard/', views.anomalyDashboard, name='anomaly-dashboard'),
    path('data/', views.get_real_time_data, name='get_real_time_data'),
]