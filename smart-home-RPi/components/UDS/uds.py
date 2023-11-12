from simulators.UDS.uds import run_uds_simulator
from sensors.UDS.DUS1 import run_dus_loop
import threading
import time


def uds_callback(distance, print_lock, uds):
    with print_lock:
        t = time.localtime()
        print("=" * 20)
        print(f"UDS: {uds}")
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(distance)

def run_dus1(settings, threads, stop_event, print_lock):
    uds = settings['name']
    if settings['simulated']:
        #print("Starting dus1 sumilator")
        dus1_thread = threading.Thread(target=run_uds_simulator, args=(2, uds_callback, stop_event, print_lock, uds))
        dus1_thread.start()
        threads.append(dus1_thread)
        #print("Dus1 sumilator started")
    else:
        print("Starting dus1 loop")
        trig_pin = settings['trig_pin']
        echo_pin = settings['trig_pin']
        dht1_thread = threading.Thread(target=run_dus_loop, args=(trig_pin, echo_pin, 2, uds_callback, stop_event, print_lock, uds))
        dht1_thread.start()
        threads.append(dht1_thread)
        print("Dus1 loop started")

