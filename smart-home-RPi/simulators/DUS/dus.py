import time
import random


def generate_values():
    distance = random.randint(0, 200)
    while True:
        distance = distance + random.randint(-30, 30)
        if distance < 0 or distance > 200:
            distance = random.randint(0, 200)
            yield 0

        yield distance


def run_uds_simulator(delay, callback, stop_event, print_lock, settings, publish_event):
    for distance in generate_values():
        time.sleep(delay)
        callback(distance, print_lock, settings, publish_event)
        if stop_event.is_set():
            break
