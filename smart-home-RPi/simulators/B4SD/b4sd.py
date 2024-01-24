import time


def generate_values():
    while True:
        n = time.ctime()[11:13] + time.ctime()[14:16]
        s = str(n).rjust(4)

        if int(time.ctime()[18:19]) % 2 == 0:
            s = s + "."
        yield s


def run_b4sd_simulator(callback, stop_event, print_lock, settings, publish_event, alarm_event):
    for message in generate_values():
        time.sleep(5)
        callback(message, print_lock, settings, publish_event, alarm_event)
        if stop_event.is_set():
            break
