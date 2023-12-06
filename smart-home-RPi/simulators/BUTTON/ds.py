import random

import keyboard
import time
from sensors.BUTTON.DS import DS


def toggle_door_sensor(ds, ds_callback, print_lock, settings, publish_event):
    ds.toggle()
    if ds.state:
        ds.turnOn()
        ds_callback(True, print_lock, settings, publish_event)
    else:
        ds.turnOff()
        ds_callback(False, print_lock, settings, publish_event)

def run_ds_simulator(ds_callback, stop_event, print_lock, settings, publish_event):
    ds = DS(settings['pin'])
    while not stop_event.is_set():
        try:
            if random.randint(0, 1) > 0.5:
                toggle_door_sensor(ds, ds_callback, print_lock, settings, publish_event)
                time.sleep(2)  # Debounce to prevent rapid toggling
            time.sleep(0.01)  # Adjust sleep time as needed for responsiveness
        except Exception as e:
            with print_lock:
                print(f"An error occurred: {e}")
                break