from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import *

# Register your models here.


class ElectricityBalanceLogResource(resources.ModelResource):

    class Meta:
        model = ElectrictyBalanceLog
        fields = ('id', 'meter_no__meter_number', 'balance', 'current_usage', 'voltage_usage', 'apparent_power', 'timestamp')

class LightSwitchResource(resources.ModelResource):

    class Meta:
        model = LightSwitch
        fields = ('id', 'meter_no__meter_number', 'current_usage', 'voltage_usage', 'apparent_power', 'timestamp')

class SocketSwitchResource(resources.ModelResource):

    class Meta:
        model = SocketSwitch
        fields = ('id', 'meter_no__meter_number', 'current_usage', 'voltage_usage', 'apparent_power', 'timestamp')


@admin.register(ElectricityBalance)
class ElectricityBalanceModelAdmin(admin.ModelAdmin):
    list_display = ['meter_no', 'balance', 'created_at', 'updated_at']
    

@admin.register(ElectrictyBalanceLog)
class ElectricityBalanceLogModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['meter_no', 'voltage_usage', 'current_usage', 'apparent_power', 'timestamp']
    list_filter = ['meter_no', 'timestamp']
    resource_classes = [ElectricityBalanceLogResource]


@admin.register(LightSwitch)
class LightSwitchModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['meter_no', 'voltage_usage', 'current_usage', 'apparent_power', 'timestamp']
    list_filter = ['meter_no', 'timestamp']
    resource_classes = [LightSwitchResource]


@admin.register(SocketSwitch)
class SocketSwitchModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['meter_no', 'voltage_usage', 'current_usage', 'apparent_power', 'timestamp']
    list_filter = ['meter_no', 'timestamp']
    resource_classes = [SocketSwitchResource]


admin.site.register(Token)


admin.site.site_header = "Prepaid and Anomaly Detection System"
admin.site.site_title = "Prepaid and Anomaly Detection System"
admin.site.index_title = "Prepaid and Anomaly Detection System"
