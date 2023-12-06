import time
import random


def simulated_keypad(print_lock, stop_event, settings, publish_event, ms_callback):
    while True:
        if stop_event.is_set():
            break
        valid_buttons = {"1", "2", "3", "A", "4", "5", "6", "B", "7", "8", "9", "C", "*", "0", "#", "D"}
        pressed_buttons = []

        for _ in range(5):
            simulated_key_press = random.choice(list(valid_buttons))
            pressed_buttons.append(simulated_key_press)
            time.sleep(2)  # Debounce delay

        if pressed_buttons:
            with print_lock:
                print("===========================================")
                print("Buttons pressed during the simulation:")
                print(", ".join(pressed_buttons))
                ms_callback(print_lock, stop_event, settings, publish_event, pressed_buttons)
        else:
            with print_lock:
                print("No buttons were pressed during the simulation.")

