
class Home(object):
    def __init__(self, pin):
        self.people_count = 0
        self.is_alarm_on = False
        self.alarm_pin = pin

    def inc_counter(self):
        self.people_count += 1

    def dec_counter(self):
        if self.people_count > 0:
            self.people_count -= 1

    def set_pin(self, pin):
        self.alarm_pin = pin
