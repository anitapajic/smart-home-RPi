import time

try:
    import RPi.GPIO as GPIO
except:
    pass

class DS(object):
    def __init__(self, pin):
        self.pin = pin
        self.state = False  # Initialize the state as off


    def toggle(self):
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.OUT)
        except:
            pass
        self.state = not self.state  # Toggle the state

    def turnOn(self):
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.OUT)
        except:
            pass
        if not self.state:
            try:
                GPIO.output(self.pin, GPIO.HIGH)
            except:
                pass

            self.state = True

    def turnOff(self):
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.OUT)
        except:
            pass
        if self.state:
            try:
                GPIO.output(self.pin, GPIO.HIGH)
            except:
                pass
            self.state = False


def run_ds_loop(callback, stop_event, print_lock, settings, publish_event):
    # Initialize the door light and button
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(settings['button_pin'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    ds = DS(settings['pin'])
    def button_callback(channel):
        ds.toggle()  # Toggle the door light
        if ds.state:
            ds.turnOn()
            callback(True, print_lock, settings, publish_event)
        else:
            ds.turnOff()
            callback(False, print_lock, settings, publish_event)

    # Add an interrupt for the button press
    GPIO.add_event_detect(settings['button_pin'], GPIO.FALLING, callback=button_callback, bouncetime=200)

    while True:
        if stop_event.is_set():
            ds.turnOff()  # Ensure the light is off when stopping
            callback(False, print_lock, settings, publish_event)
            break

        # Sleep for a short period to allow handling of button presses
        time.sleep(0.1)
