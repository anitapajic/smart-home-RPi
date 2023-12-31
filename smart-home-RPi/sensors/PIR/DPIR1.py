import time
try:
    import RPi.GPIO as GPIO
except:
    pass


def real_pir(PIR_PIN, pir_name, print_lock, stop_event, settings, publish_event, pir_callback, home, event, light_event=None):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIR_PIN, GPIO.IN)

    def motion_detected_callback(channel):
        print("DPIR1 detected movement!")
        event.set()
        pir_callback(pir_name, print_lock, stop_event, settings, publish_event, 1, light_event)

    def motion_ended_callback(channel):
        pir_callback(pir_name, print_lock, stop_event, settings, publish_event, 0, light_event)
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
