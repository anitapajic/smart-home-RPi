from  simulators.LED_DIODE.led_diode import run_dl_simulator
from sensors.LED_DIODE.DL import run_dl_loop
import threading
import time


def dl_callback(state, print_lock, dl):
    with print_lock:
        t = time.localtime()
        print("=" * 20)
        print(f"DL: {dl}")
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"State: {state}")


def run_dl(settings, threads, stop_event, print_lock):
    dl_name = settings['name']
    if settings['simulated']:
        print("Starting dl sumilator")
        dl_pin = settings['pin']
        dl_thread = threading.Thread(target=run_dl_simulator, args=(dl_pin, dl_callback, stop_event, print_lock, dl_name))
        dl_thread.start()
        threads.append(dl_thread)
        print("Dl sumilator started")
        print("Press m to switch light")
    else:
        from sensors.LED_DIODE.DL import run_dl_loop, DL
        print("Starting dl loop")
        dl_pin = settings['pin']
        button_pin = settings['button_pin']
        dl_thread = threading.Thread(target=run_dl_loop, args=(button_pin, dl_pin, dl_callback, stop_event, print_lock, dl_name))
        dl_thread.start()
        threads.append(dl_thread)
        print("Dl loop started")