
import threading
from settings import load_settings
from components.DHT.dht import run_dht1, run_dht2
from components.LED_DIODE.led_diode import run_dl
import time
from threading import Lock

print_lock = Lock()


try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass


if __name__ == "__main__":
    print('Starting app')
    settings = load_settings()
    threads = []
    stop_event = threading.Event()
    try:
        # dht1_settings = settings['DHT1']
        # run_dht1(dht1_settings, threads, stop_event, print_lock)
        # dht2_settings = settings['DHT2']
        # run_dht2(dht2_settings, threads, stop_event, print_lock)
        dl_settings = settings['DL']
        run_dl(dl_settings, threads, stop_event, print_lock)
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()
