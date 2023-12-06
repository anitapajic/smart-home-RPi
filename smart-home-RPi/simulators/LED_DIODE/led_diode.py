import random

import keyboard
import time
from sensors.LED_DIODE.DL import DL


def toggle_door_light(dl, dl_callback, print_lock, settings, publish_event):
    dl.toggle()
    if dl.state:
        dl.turnOn()
        dl_callback(True, print_lock, settings, publish_event)
    else:
        dl.turnOff()
        dl_callback(False, print_lock, settings, publish_event)


def run_dl_simulator(dl_callback, stop_event, print_lock, settings, publish_event):
    dl = DL(settings['pin'])
    while not stop_event.is_set():
        try:
            if keyboard.is_pressed('m'):
                toggle_door_light(dl, dl_callback, print_lock, settings, publish_event)
                time.sleep(0.2)  # Debounce to prevent rapid toggling
            time.sleep(0.01)  # Adjust sleep time as needed for responsiveness
        except Exception as e:
            with print_lock:
                print(f"An error occurred: {e}")
                break


