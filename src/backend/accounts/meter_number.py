import random

def generate_meter_number(existing_numbers):
    prefix = '371'
    while True:
        # generate 9 random digits
        unique_part = ''.join(random.choices('0123456789', k=9))
        meter_number = int(prefix + unique_part)
        # ensure the meter number is unique
        if meter_number not in existing_numbers:
            existing_numbers.add(meter_number)
            return meter_number