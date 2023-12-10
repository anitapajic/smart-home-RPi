import time

import random

def generate_values():
    while True:
        temperature = random.randint(-20, 40)  # Random temperature between -20 and 40 degrees Celsius
        humidity = random.randint(0, 100)  # Random humidity percentage between 0 and 100
        yield f"Temperature: {temperature} °C\nHumidity: {humidity}%"


def run_lcd_simulator(callback, stop_event, print_lock, settings, publish_event):
    for message in generate_values():
        time.sleep(1)
        callback(message, print_lock, settings, publish_event)
        if stop_event.is_set():
            break
