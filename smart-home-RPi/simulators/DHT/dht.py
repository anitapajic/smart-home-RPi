
import time
import random


def generate_values(initial_temp=25, initial_humidity=20):
    temperature = initial_temp
    humidity = initial_humidity
    while True:
        temperature = temperature + random.randint(-1, 1)
        humidity = humidity + random.randint(-1, 1)
        if humidity < 0:
            humidity = 0
        if humidity > 100:
            humidity = 100
        yield humidity, temperature


def run_dht_simulator(delay, callback, stop_event, print_lock, dht):
    # Simulate some status code, e.g., 0 for success
    code = 0
    for h, t in generate_values():
        time.sleep(delay)  # Delay between readings
        # Now pass the code as well, assuming code=0 means success
        callback(h, t, code, print_lock, dht)
        if stop_event.is_set():
            break
