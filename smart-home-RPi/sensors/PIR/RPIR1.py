
try:
    import RPi.GPIO as GPIO
except:
    pass


def motion_detected(channel):
    print("RPIR1 detected movement!")


def no_motion(channel):
    print("You stopped moving")


def real_pir(PIR_PIN):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIR_PIN, GPIO.IN)

    GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=motion_detected)
    # GPIO.add_event_detect(PIR_PIN, GPIO.FALLING, callback=no_motion)

    input("Press any key to exit...")