import time
import random


def generate_values():
    distance = random.randint(0, 200)

    while True:
        distance = distance + random.randint(-30, 30)
        new_distance = distance + random.randint(-10, 10)

        if distance < 0 or distance > 200:
            distance = random.randint(0, 200)
            new_distance = distance + random.randint(-10, 10)
            yield 0, 0

        yield distance, new_distance


def run_dus_simulator(delay, callback, stop_event, print_lock, settings, publish_event, home, event):
    for distance, new_distance in generate_values():
        event.wait()
        if new_distance < distance:
            with print_lock:
                home.inc_counter()
        else:
            with print_lock:
                home.dec_counter()

        callback(distance, print_lock, settings, publish_event)
        callback(new_distance, print_lock, settings, publish_event)
        event.clear()
        if stop_event.is_set():
            break
        time.sleep(delay)
