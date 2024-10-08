import json

from django.shortcuts import get_object_or_404

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from accounts.models import AccountMeter
from balances.models import ElectricityBalance, ElectrictyBalanceLog


class PrepaidBalanceConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        # print(self.scope)
        meter_number = self.scope['url_route']['kwargs']['meter_number']
        self.meter_number = meter_number

        self.room_group_name = f'balance-{meter_number}'
    
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        # Send a message to the WebSocket
        # await self.send(text_data="The WebSocket has successfully connected")


    async def disconnect(self, close_code):
        print(f'disconnected with close code: {close_code}')

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):
        
        balance = json.loads(text_data)

        consumed_electricty = balance["consumed_electricity"]

        await self.save_updated_data(self.meter_number, consumed_electricty)

        balance = await self.get_current_electricity_balance(self.meter_number)

        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'current_electricty_balance',
            'balance': balance
        })


    async def current_electricty_balance(self, event):

        balance = event['balance']

        await self.send(text_data=json.dumps({
            'meter_no': f'{self.meter_number}',
            'balance': balance
        }))


    @database_sync_to_async
    def update_balance(self, meter_no, consumed_power):
        meter = get_object_or_404(AccountMeter, meter_number=meter_no)
        obj = get_object_or_404(ElectricityBalance, meter_no=meter)
        current_balance = obj.balance - consumed_power
        obj.balance = current_balance
        obj.save()

    
    async def save_updated_data(self, meter_no, consumed_power):
        await self.update_balance(meter_no, consumed_power)


    @database_sync_to_async
    def fetch_current_balance(self, meter_no):
        meter = get_object_or_404(AccountMeter, meter_number=meter_no)
        obj = get_object_or_404(ElectricityBalance, meter_no=meter)
        return obj.balance
    

    async def get_current_electricity_balance(self, meter_number):
        balance = await self.fetch_current_balance(meter_number)
        return round(balance, 1)
        


class ElectricityConsumptionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        meter_number = self.scope['url_route']['kwargs']['meter_number']
        self.meter_number = meter_number

        self.room_group_name = f'consumption-{meter_number}'
    
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()


    async def receive(self, text_data=None, bytes_data=None):
        consumption = json.loads(text_data)

        current = consumption["irms"]
        voltage = consumption['voltage']
        apparent_power = consumption['apparent_power']

        await self.save_consumption_data(self.meter_number, voltage, current, apparent_power)

        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'consumption_status',
            'Recieved': True
        })

    
    async def consumption_status(self, event):

        consumption = event['Recieved']

        await self.send(text_data=json.dumps({
            'meter_no': f'{self.meter_number}',
            'Recieved': consumption
        }))
        

    async def disconnect(self, close_code):
        print(f'disconnected with close code: {close_code}')

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def save_consumption_data(self, meter_no, voltage, irms, apparent_power):
        await self.update_consumption(meter_no, voltage, irms, apparent_power)

    
    @database_sync_to_async
    def update_consumption(self, meter_no, voltage, irms, apparent_power):
        meter = get_object_or_404(AccountMeter, meter_number=meter_no)
        
        ElectrictyBalanceLog.objects.create(
            meter_no=meter,
            current_usage = irms,
            voltage_usage =voltage,
            apparent_power=apparent_power,
            balance=None
        )

