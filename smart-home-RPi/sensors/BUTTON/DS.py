import time

try:
    import RPi.GPIO as GPIO
except:
    pass

class DS(object):
    def __init__(self, pin):
        self.pin = pin
        self.state = False  # Initialize the state as off
        self.time = 11703882722

    def toggle(self):
        self.state = not self.state  # Toggle the state

    def turn_on_sim(self):
        self.state = True
        if self.time > time.time():
            self.time = time.time()

    def turn_off_sim(self):
        self.state = False
        self.time = 11703882722

    def turnOn(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        if not self.state:
            GPIO.output(self.pin, GPIO.HIGH)
            self.state = True
            if self.time > time.time():
                self.time = time.time()
    def turnOff(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        if self.state:
            GPIO.output(self.pin, GPIO.LOW)
            self.state = False
            self.time = 11703882722

def run_ds_loop(callback, stop_event, print_lock, settings, publish_event, alarm_ds, switch, ds_event, home, switch_off):
    # Initialize the door light and button
    GPIO.setmode(GPIO.BCM)
    ds = DS(settings['pin'])
    while True:
        switch.wait()

        ds.turnOn()  # kada pusti treba ds.turnOff() i alarm_ds.clear()
        callback(ds.state, print_lock, settings, publish_event)

        if time.time() - ds.time > 5:
            alarm_ds.set()
            home.alarm = True
        switch.clear()

        if stop_event.is_set():
            ds.turnOff()  # Ensure the light is off when stopping
            callback(False, print_lock, settings, publish_event)
            alarm_ds.clear()
            break

        # Sleep for a short period to allow handling of button presses
        time.sleep(0.1)

