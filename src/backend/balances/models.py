
from django.db import models

from balances.model_utils import generate_random_voltage
from payments.models import Payment
from accounts.models import AccountMeter

# Create your models here.

class Token(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.PROTECT, related_name='token_payment')

    meter_no = models.ForeignKey(AccountMeter, on_delete=models.CASCADE, null=True)
    token = models.PositiveIntegerField(unique=True)

    is_used = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.token)
    

class ElectricityBalance(models.Model):
    meter_no = models.OneToOneField(AccountMeter, on_delete=models.CASCADE, null=True, related_name='meter_balance')
    balance = models.FloatField(null=True, default=0)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.balance)
    

class ElectrictyBalanceLog(models.Model):
    meter_no = models.ForeignKey(AccountMeter, on_delete=models.CASCADE, null=True)
    balance = models.FloatField(null=True)
    current_usage = models.FloatField(null=True)
    voltage_usage = models.FloatField(null=True)
    apparent_power = models.FloatField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.balance)
    

class LightSwitch(models.Model):
    meter_no = models.ForeignKey(AccountMeter, on_delete=models.CASCADE, null=True)
    current_usage = models.FloatField(null=True)
    voltage_usage = models.FloatField(null=True, default=generate_random_voltage)
    apparent_power = models.FloatField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.current_usage}A - {self.voltage_usage}V '


class SocketSwitch(models.Model):
    meter_no = models.ForeignKey(AccountMeter, on_delete=models.CASCADE, null=True)
    current_usage = models.FloatField(null=True)
    voltage_usage = models.FloatField(null=True, default=generate_random_voltage)
    apparent_power = models.FloatField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.current_usage}A - {self.voltage_usage}V '
    

    def save(self, *args, **kwargs):
        # Calculate the apparent power as voltage * current
        if self.current_usage is not None and self.voltage_usage is not None:
            self.apparent_power = self.current_usage * self.voltage_usage
        else:
            self.apparent_power = None
        
        # Call the original save method to persist the data
        super(SocketSwitch, self).save(*args, **kwargs)
