import time
import random


def simulated_ir(print_lock, stop_event, bir_settings, publish_event, ir_callback, rgb_queue):
    while True:
        if stop_event.is_set():
            break
        ButtonsNames = ["UP", "DOWN", "2", "3", "1", "4", "5", "6", "7"]
        button = random.choice(list(ButtonsNames))
        if rgb_queue:
            rgb_queue.put(button)
        ir_callback(bir_settings, publish_event, button)
        with print_lock:
            print("PRITISNUTO DUGME: ", button)
        time.sleep(1)
