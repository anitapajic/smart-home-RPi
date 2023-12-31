import time

try:
    import RPi.GPIO as GPIO
except:
    pass
class DUS(object):
    def __init__(self, trig_pin, echo_pin):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(TRIG_PIN, GPIO.OUT)
        # GPIO.setup(ECHO_PIN, GPIO.IN)
    def get_distance(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

        GPIO.output(self.trig_pin, False)
        time.sleep(0.2)
        GPIO.output(self.trig_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trig_pin, False)
        pulse_start_time = time.time()
        pulse_end_time = time.time()

        max_iter = 100

        iter = 0
        while GPIO.input(self.echo_pin) == 0:
            if iter > max_iter:
                return None
            pulse_start_time = time.time()
            iter += 1

        iter = 0
        while GPIO.input(self.echo_pin) == 1:
            if iter > max_iter:
                return None
            pulse_end_time = time.time()
            iter += 1

        pulse_duration = pulse_end_time - pulse_start_time
        distance = (pulse_duration * 34300)/2
        return distance

def run_dus_loop(delay, callback, stop_event, print_lock, settings, publish_event, home, event ):
    dus = DUS(settings["trig_pin"], settings["echo_pin"])
    while True:
        distance = dus.get_distance()
        callback(distance, print_lock, settings, publish_event)

        event.wait()
        new_distance = dus.get_distance()
        if new_distance < distance:
            with print_lock:
                home.inc_counter()
        else:
            with print_lock:
                home.dec_counter()
        callback(new_distance, print_lock, settings, publish_event)
        event.clear()

        if stop_event.is_set():
            break
        time.sleep(delay)
