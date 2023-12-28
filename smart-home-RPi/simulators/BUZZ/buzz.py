import time


def simulated_buzz(pitch, duration, settings, publish_event, buzz_callback):
    try:
        import winsound
        winsound.Beep(pitch, duration)
        buzz_callback(settings, publish_event, 1)
    except ImportError:
        print("winsound module is not available on this system.")


def listen_for_keypress(stop_event, print_lock, pitch, duration, settings, publish_event, buzz_callback, alarm):
    while not stop_event.is_set():
        alarm.wait()
        with print_lock:
            print("Buzzer activated!")
        time.sleep(1)
        simulated_buzz(pitch, duration, settings, publish_event, buzz_callback)
        alarm.clear()
