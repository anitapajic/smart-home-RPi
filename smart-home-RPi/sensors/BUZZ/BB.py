import time


def real_buzz(buzzer_pin, pitch, duration):
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzer_pin, GPIO.OUT)
    period = 1.0 / pitch
    delay = period / 2
    cycles = int(duration * pitch)
    for i in range(cycles):
        GPIO.output(buzzer_pin, True)
        time.sleep(delay)
        GPIO.output(buzzer_pin, False)
        time.sleep(delay)
    GPIO.cleanup(buzzer_pin)


def bb_loop(buzzer_pin, pitch, duration, settings, publish_event, buzz_callback, alarm_event, alarm_clock_event):
    try:
        import RPi.GPIO as GPIO
        while True:
            events_triggered = [alarm_event.wait(timeout=1), alarm_clock_event.wait(timeout=1)]
            if events_triggered[0]:
                real_buzz(buzzer_pin, pitch, duration)
                time.sleep(1)
                if not alarm_event.is_set():
                    buzz_callback(settings, publish_event, 1)
            elif events_triggered[1]:
                real_buzz(buzzer_pin, pitch, duration)
                time.sleep(1)
                if not alarm_clock_event.is_set():
                    buzz_callback(settings, publish_event, 1)
    except KeyboardInterrupt:
        GPIO.cleanup()


