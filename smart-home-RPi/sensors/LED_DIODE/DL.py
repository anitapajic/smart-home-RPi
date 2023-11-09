import time

try:
    import RPi.GPIO as GPIO
except:
    pass

class DL(object):
    def __init__(self, pin):
        self.pin = pin
        self.state = False  # Initialize the state as off


    def toggle(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.state = not self.state  # Toggle the state

    def turnOn(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        if not self.state:
            GPIO.output(self.pin, GPIO.HIGH)
            self.state = True

    def turnOff(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        if self.state:
            GPIO.output(self.pin, GPIO.LOW)
            self.state = False


def run_dl_loop(button_pin, dl_pin, callback, stop_event, print_lock, dl_name):
    # Initialize the door light and button
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    dl = DL(dl_pin)
    def button_callback(channel):
        dl.toggle()  # Toggle the door light
        if dl.state:
            dl.turnOn()
            callback("Door Light is ON", print_lock, dl_name)
        else:
            dl.turnOff()
            callback("Door Light is OFF", print_lock, dl_name)

    # Add an interrupt for the button press
    GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_callback, bouncetime=200)

    while True:
        if stop_event.is_set():
            dl.turnOff()  # Ensure the light is off when stopping
            callback("Door Light is OFF", print_lock, dl_name)
            break

        # Sleep for a short period to allow handling of button presses
        time.sleep(0.1)