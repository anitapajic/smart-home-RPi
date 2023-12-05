import random
import time


def simulated_motion_detected(name, print_lock):
    with print_lock:
        print("------------------------------------")
        print(f"{name} Sensor detected movement!")
        print("------------------------------------")


def simulated_no_motion(name, print_lock):
    with print_lock:
        print("------------------------------------")
        print(f"{name} Sensor detected no motion!")
        print("------------------------------------")


def simulated_pir(name, print_lock, stop_event, settings, publish_event, callback):
    try:
        while True:
            if random.randint(-1, 1) > 0:
                simulated_motion_detected(name, print_lock)
                callback(name, print_lock, stop_event, settings, publish_event, 1)
            else:
                simulated_no_motion(name, print_lock)
                callback(name, print_lock, stop_event, settings, publish_event, 0)
            time.sleep(3)
            if stop_event.is_set():
                break

    except KeyboardInterrupt:
        print("\nSimulated PIR sensor stopped!")
