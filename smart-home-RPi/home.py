
class Home(object):
    def __init__(self, pin, time=None):
        self.people_count = 0
        self.is_alarm_on = False
        self.alarm_pin = pin
        self.safety_system = False
        self.alarm = False
        self.alarm_clock = time

    def inc_counter(self):
        self.people_count += 1

    def dec_counter(self):
        if self.people_count > 0:
            self.people_count -= 1

    def set_pin(self, pin):
        self.alarm_pin = pin
        self.safety_system = True

    def deactivate_safety_system(self):
        self.safety_system = False

    def set_alarm_clock(self, time):
        self.alarm_clock = time

    def turn_off_clock(self):
        self.alarm_clock = None
