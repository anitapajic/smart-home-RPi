import time


def generate_values():
    while True:
        yield time.strftime("%H:%M:%S", time.gmtime())


def run_lcd_simulator(callback, stop_event, print_lock, settings, publish_event):
    for message in generate_values():
        time.sleep(1)
        callback(message, print_lock, settings, publish_event)
        if stop_event.is_set():
            break
