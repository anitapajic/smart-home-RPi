import time


def simulated_keypad():
    valid_buttons = {"1", "2", "3", "A", "4", "5", "6", "B", "7", "8", "9", "C", "*", "0", "#", "D"}
    pressed_buttons = []

    print("Press a button or type 'q' to exit.")
    while True:
        key_press = input(">> ").upper()
        if key_press in valid_buttons:
            print(f"Keypad button {key_press} pressed")
            pressed_buttons.append(key_press)
        elif key_press == 'Q':
            print("Exiting keypad simulation.")
            break
        else:
            print("Invalid button. Please press a valid button.")
        time.sleep(0.2)  # Debounce delay

    if pressed_buttons:
        print("Buttons pressed during the simulation:")
        print(", ".join(pressed_buttons))
    else:
        print("No buttons were pressed during the simulation.")
