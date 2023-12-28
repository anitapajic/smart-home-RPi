import time


def simulated_keypad(print_lock, stop_event, settings, publish_event, ms_callback):
    while True:
        if stop_event.is_set():
            break
        valid_buttons = {"1", "2", "3", "A", "4", "5", "6", "B", "7", "8", "9", "C", "*", "0", "D", "#"}
        pressed_buttons = []

        with print_lock:
            print("Enter 4 character and last one '#':")
            while len(pressed_buttons) < 5:
                key_press = input("Enter one character: ").strip()
                if key_press == 'q':
                    break
                if key_press in valid_buttons:
                    pressed_buttons.append(key_press)
                    if key_press == '#':  # Prekid unosa nakon '#'
                        break
                else:
                    print("Not valid character.")

        if pressed_buttons:
            code = "".join(pressed_buttons)
            ms_callback(print_lock, stop_event, settings, publish_event, code)
            with print_lock:
                print("Code pressed: ", code)
        else:
            with print_lock:
                print("No buttons were pressed during the simulation.")

        time.sleep(10)
