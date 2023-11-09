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


def simulated_pir(name, print_lock):
    try:
        while True:
            if random.randint(-1, 1) > 0:
                simulated_motion_detected(name, print_lock)
            else:
                simulated_no_motion(name, print_lock)
            time.sleep(2)

    except KeyboardInterrupt:
        print("\nSimulated PIR sensor stopped!")
