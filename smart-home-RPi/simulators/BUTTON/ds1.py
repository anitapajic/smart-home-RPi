import random

import keyboard
import time
from sensors.BUTTON.DS1 import DS


def toggle_door_sensor(dl, dl_callback, print_lock, dl_name):
    dl.toggle()
    if dl.state:
        dl.turnOn()
        dl_callback("Door Sensor is ON", print_lock, dl_name)
    else:
        dl.turnOff()
        dl_callback("Door Sensor is OFF", print_lock, dl_name)


def run_ds_simulator(dl_pin, dl_callback, stop_event, print_lock, dl_name):
    dl = DS(dl_pin)
    while not stop_event.is_set():
        try:
            if random.randint(0, 1) > 0.5:
                toggle_door_sensor(dl, dl_callback, print_lock, dl_name)
                time.sleep(2)  # Debounce to prevent rapid toggling
            time.sleep(0.01)  # Adjust sleep time as needed for responsiveness
        except Exception as e:
            with print_lock:
                print(f"An error occurred: {e}")
                break