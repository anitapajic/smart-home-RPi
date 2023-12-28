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


def simulated_pir(name, print_lock, stop_event, settings, publish_event, callback, home, event, light_event=None):
    try:
        while True:
            if random.randint(-1, 1) > 0:
                simulated_motion_detected(name, print_lock)
                callback(name, print_lock, stop_event, settings, publish_event, 1, light_event)
                if home.people_count == 0 and "Room PIR" in name:
                    with print_lock:
                        event.set()    # u room pir to je alarm event
                if "Door PIR" in name:
                    event.set()        # u door pir je counter event
            else:
                # simulated_no_motion(name, print_lock)
                callback(name, print_lock, stop_event, settings, publish_event, 0, None)
            time.sleep(10)
            if stop_event.is_set():
                break

    except KeyboardInterrupt:
        print("\nSimulated PIR sensor stopped!")
