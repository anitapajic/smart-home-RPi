import time

def enter_pin(print_lock, stop_event, settings, publish_event, ms_callback, home, alarm, ds_event, my_time=None):
    valid_buttons = {"1", "2", "3", "A", "4", "5", "6", "B", "7", "8", "9", "C", "*", "0", "D", "#"}
    pressed_buttons = []
    wrong_pin = True
    while wrong_pin:
        if my_time is not None:
            if time.time() - my_time >= 10:
                print("too long")
                ds_event.clear()
                alarm.set()
                wrong_pin = False

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
            print(code, " code and ", home.alarm_pin, " alarm pin")
            if not home.alarm and not home.safety_system:  # ako se pin unosi dok nema alarma to je za postavljanje sigurnosnog sistema (ili izmeni da kad stavi * na kraj da je za ovo)
                home.set_pin(code)
                home.safety_system = True

            if home.alarm or home.safety_system:  # pin sluzi za deaktivaciju alarma i/ili sigurnosnog sistema
                if code == home.alarm_pin:
                    home.safety_system = False
                    home.alarm = False
                    wrong_pin = False
                    pressed_buttons = []
                    print("Alarm turned off")
                    ds_event.clear()
                    alarm.clear()
                else:
                    print("=========WRONG PIN=========")
                    pressed_buttons = []


            ms_callback(print_lock, stop_event, settings, publish_event, code)
            with print_lock:
                print("Code pressed: ", code)
        else:
            with print_lock:
                print("No buttons were pressed during the simulation.")


def simulated_keypad(print_lock, stop_event, settings, publish_event, ms_callback, home, alarm, ds_event):
    while True:
        if stop_event.is_set():
            break

        events_triggered = [ds_event.wait(timeout=1), alarm.wait(timeout=1)]

        if events_triggered[0]:  # ds_event is set
            print("DS PIN")
            enter_pin(print_lock, stop_event, settings, publish_event, ms_callback, home, alarm, ds_event, time.time())
        elif events_triggered[1]:  # alarm event is set
            print("ALARM PIN")
            enter_pin(print_lock, stop_event, settings, publish_event, ms_callback, home, alarm, ds_event)


