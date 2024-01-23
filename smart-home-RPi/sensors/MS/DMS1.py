import time


try:
    import RPi.GPIO as GPIO
except:
    pass
# GPIO pin assignments
R1 = 25
R2 = 8
R3 = 7
R4 = 1
C1 = 12
C2 = 16
C3 = 20
C4 = 21

# Setup GPIO pins
def setup_gpio():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(R1, GPIO.OUT)
    GPIO.setup(R2, GPIO.OUT)
    GPIO.setup(R3, GPIO.OUT)
    GPIO.setup(R4, GPIO.OUT)

    GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# Function to read a single line
def read_line(line, characters):
    GPIO.output(line, GPIO.HIGH)
    if GPIO.input(C1) == 1:
        print(characters[0])
    if GPIO.input(C2) == 1:
        print(characters[1])
    if GPIO.input(C3) == 1:
        print(characters[2])
    if GPIO.input(C4) == 1:
        print(characters[3])
    GPIO.output(line, GPIO.LOW)


# Function to read from the keypad
def real_keypad(print_lock, stop_event, settings, publish_event, ms_callback, home, alarm, ds_event):
    setup_gpio()
    accumulated_keys = ''  # Variable to accumulate keypresses
    try:
        while True:
            alarm.wait()
            for line, characters in [(R1, ["1", "2", "3", "A"]),
                                     (R2, ["4", "5", "6", "B"]),
                                     (R3, ["7", "8", "9", "C"]),
                                     (R4, ["*", "0", "#", "D"])]:
                keypress = read_line(line, characters)
                if keypress:
                    print(keypress)  # Print the keypress
                    accumulated_keys += keypress  # Add keypress to the accumulated string

                    # Check if the accumulated keys form a complete code
                    if len(accumulated_keys) == 5:
                        ms_callback(print_lock, stop_event, settings, publish_event, accumulated_keys)
                        if home.alarm or home.safety_system:  # pin sluzi za deaktivaciju alarma i/ili sigurnosnog sistema
                            if accumulated_keys == home.alarm_pin:
                                home.safety_system = False
                                home.alarm = False
                                alarm.clear()

                        if not home.alarm:  # ako se pin unosi dok nema alarma to je za postavljanje sigurnosnog sistema (ili izmeni da kad stavi * na kraj da je za ovo)
                            home.set_pin(accumulated_keys)
                            home.safety_system = True

                        accumulated_keys = ''  # Reset for the next code


            time.sleep(0.2)
    except KeyboardInterrupt:
        print("\nApplication stopped!")
    finally:
        GPIO.cleanup()