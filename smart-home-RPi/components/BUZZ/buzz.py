import threading
from simulators.BUZZ.buzz import simulated_buzz, listen_for_keypress
from sensors.BUZZ.DB import real_buzz


def run_db1(settings, threads, stop_event, print_lock):
    pitch = settings.get('pitch', 440)  # Default to 440 if not set
    duration = settings.get('duration', 1000)  # Default to 1 if not set

    if settings['simulated']:
        print("Starting buzzer simulator")
        buzzer_thread = threading.Thread(target=listen_for_keypress, args=(stop_event, print_lock, pitch, duration))
        buzzer_thread.start()
        threads.append(buzzer_thread)
        print("Buzzer simulator started")
    else:
        print("Starting real buzzer")
        buzzer_pin = settings['pin']
        buzzer_thread = threading.Thread(target=buzz_loop, args=(buzzer_pin, 440, 1))
        buzzer_thread.start()
        threads.append(buzzer_thread)
        print("Real buzzer started")

