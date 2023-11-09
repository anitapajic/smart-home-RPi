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
def real_keypad(stop_event):
    setup_gpio()

    try:
        while not stop_event.is_set():
            read_line(R1, ["1", "2", "3", "A"])
            read_line(R2, ["4", "5", "6", "B"])
            read_line(R3, ["7", "8", "9", "C"])
            read_line(R4, ["*", "0", "#", "D"])
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("\nApplication stopped!")
    finally:
        GPIO.cleanup()