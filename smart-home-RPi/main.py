import sys
import threading
from settings import load_settings
from components.DHT.dht import run_dht
from components.BUTTON.ds1 import run_ds
from components.DUS.dus import run_dus
from threading import Lock
from components.MS.ms import run_keypad
from components.PIR.pir import run_RPIR1, run_RPIR2, run_DPIR1

print_lock = Lock()


try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass


def run_simulators(stop_event):
    # STOP
    enter_thread = threading.Thread(target=listen_for_stop_command, args=(stop_event,))
    enter_thread.start()
    # DHT
    dht1_settings = settings['DHT1']
    run_dht(dht1_settings, threads, stop_event, print_lock)
    dht2_settings = settings['DHT2']
    run_dht(dht2_settings, threads, stop_event, print_lock)
    dht3_settings = settings['DHT3']
    run_dht(dht3_settings, threads, stop_event, print_lock)
    dht4_settings = settings['DHT4']
    run_dht(dht4_settings, threads, stop_event, print_lock)
    gdht_settings = settings['GDHT']
    run_dht(gdht_settings, threads, stop_event, print_lock)

    # PIR
    rpir1_settings = settings['RPIR1']
    run_RPIR1(rpir1_settings, threads, stop_event, print_lock)
    rpir2_settings = settings['RPIR2']
    run_RPIR2(rpir2_settings, threads, stop_event, print_lock)
    dpir1_settings = settings['DPIR1']
    run_DPIR1(dpir1_settings, threads, stop_event, print_lock)

    ds1_settings = settings['DS1']
    run_ds(ds1_settings, threads, stop_event, print_lock)
    # DUS
    dus1_settings = settings['DUS1']
    run_dus(dus1_settings, threads, stop_event, print_lock)
    dus2_settings = settings['DUS2']
    run_dus(dus2_settings, threads, stop_event, print_lock)
    # MS
    dms1_settings = settings['DMS1']
    run_keypad(dms1_settings, threads, stop_event, print_lock)

    for thread in threads:
        thread.join()


def listen_for_stop_command(stop_event):
    command = input("Press '0' to stop all simulations...\n")
    if command == '0':
        for t in threads:
            stop_event.set()
        sys.exit(0)


if __name__ == "__main__":
    print('Starting app')
    settings = load_settings()
    threads = []
    stop_event = threading.Event()
    try:
        run_simulators(stop_event)
        stop_event.clear()
        threads = []

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()
