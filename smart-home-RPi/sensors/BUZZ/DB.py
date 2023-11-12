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


def buzz_loop(buzzer_pin, pitch, duration):
    try:
        while True:
            real_buzz(buzzer_pin, pitch, duration)
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()


