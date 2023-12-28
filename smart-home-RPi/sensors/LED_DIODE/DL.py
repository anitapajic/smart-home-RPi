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
        self.state = not self.state  # Toggle the state

    def turn_on_sim(self):
        self.state = True

    def turn_off_sim(self):
        self.state = False

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


def run_dl_loop(callback, stop_event, print_lock, settings, publish_event, light_event):
    # Initialize the door light and button
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(settings['button_pin'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    dl = DL(settings['pin'])

    while True:
        light_event.wait()
        if dl.state:
            dl.turnOn()
            time.sleep(10)
            dl.turnOff()
        callback(dl.state, print_lock, settings, publish_event)
        light_event.clear()

        if stop_event.is_set():
            dl.turnOff()  # Ensure the light is off when stopping
            callback(False, print_lock, settings, publish_event)
            break

        # Sleep for a short period to allow handling of button presses
        time.sleep(0.1)
