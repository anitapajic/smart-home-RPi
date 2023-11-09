import threading
from simulators.MS.ms import simulated_keypad
from sensors.MS.DMS1 import real_keypad


# Function to start the correct keypad based on settings
def run_keypad(settings, threads, stop_event, print_lock):
    if settings['simulated']:
        print("Starting keypad simulator")
        keypad_thread = threading.Thread(target=simulated_keypad)
        keypad_thread.start()
        threads.append(keypad_thread)
    else:
        print("Starting real keypad")
        keypad_thread = threading.Thread(target=real_keypad, args=(stop_event,))
        keypad_thread.start()
        threads.append(keypad_thread)