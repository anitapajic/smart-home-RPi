import time
try:
    import RPi.GPIO as GPIO
except:
    pass


def real_pir(PIR_PIN, pir_name, print_lock, stop_event, settings, publish_event, pir_callback, home, alarm):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIR_PIN, GPIO.IN)

    def motion_detected_callback(channel):
        print("RPIR3 detected movement!")
        pir_callback(pir_name, print_lock, stop_event, settings, publish_event, 1)
        if home.people_count == 0:
            alarm.set()
            home.alarm = True
    def motion_ended_callback(channel):
        pir_callback(pir_name, print_lock, stop_event, settings, publish_event, 0)
        print("You stopped moving")

    GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=motion_detected_callback)
    # GPIO.add_event_detect(PIR_PIN, GPIO.FALLING, callback=motion_ended_callback)

    try:
        while not stop_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nReal PIR sensor stopped!")
    finally:
        GPIO.cleanup()  