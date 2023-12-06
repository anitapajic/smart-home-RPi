import threading
import time
import keyboard


def simulated_buzz(pitch, duration, settings, publish_event, buzz_callback):
    try:
        import winsound
        winsound.Beep(pitch, duration)
        buzz_callback(settings, publish_event, 1)
    except ImportError:
        print("winsound module is not available on this system.")


def listen_for_keypress(stop_event, print_lock, pitch, duration, settings, publish_event, buzz_callback, key='x'):
    print(f"Press '{key}' to activate the simulated buzzer.")
    while not stop_event.is_set():
        try:
            if stop_event.is_set():
                break
            if keyboard.is_pressed(key):
                with print_lock:
                    print("Buzzer activated!")
                simulated_buzz(pitch, duration, settings, publish_event, buzz_callback)
                # buzz_callback(settings, publish_event, True)
                time.sleep(1)

        except Exception as e:
            with print_lock:
                print(f"An error occurred: {e}")
                break