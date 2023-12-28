import time

import random



def run_lcd_simulator(callback, stop_event, print_lock, settings, publish_event, queue):
    while True:
        h, t = queue.get()
        time.sleep(1)
        callback(f"Temperature: {t} °C\nHumidity: {h}%", print_lock, settings, publish_event)
        if stop_event.is_set():
            break
