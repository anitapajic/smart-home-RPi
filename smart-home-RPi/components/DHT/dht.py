from simulators.DHT.dht import run_dht_simulator
import threading
import time


def dht_callback(humidity, temperature, code, print_lock, dht):
    with print_lock:
        t = time.localtime()
        print("=" * 20)
        print(f"DHT: {dht}")
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Humidity: {humidity}%")
        print(f"Temperature: {temperature}°C")


def run_dht1(settings, threads, stop_event, print_lock):
    dht = settings['name']
    if settings['simulated']:
        print("Starting dht1 sumilator")
        dht1_thread = threading.Thread(target=run_dht_simulator, args=(2, dht_callback, stop_event, print_lock, dht))
        dht1_thread.start()
        threads.append(dht1_thread)
        print("Dht1 sumilator started")
    else:
        from sensors.DHT.RDHT1 import run_dht_loop, DHT
        print("Starting dht1 loop")
        dht = DHT(settings['pin'])
        dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, dht_callback, stop_event, print_lock))
        dht1_thread.start()
        threads.append(dht1_thread)
        print("Dht1 loop started")


def run_dht2(settings, threads, stop_event, print_lock):
    dht = settings['name']
    if settings['simulated']:
        print("Starting dht2 sumilator")
        dht1_thread = threading.Thread(target=run_dht_simulator, args=(2, dht_callback, stop_event, print_lock, dht))
        dht1_thread.start()
        threads.append(dht1_thread)
        print("Dht1 sumilator started")
    else:
        from sensors.DHT.RDHT2 import run_dht_loop, DHT
        print("Starting dht2 loop")
        dht = DHT(settings['pin'])
        dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, dht_callback, stop_event, print_lock))
        dht1_thread.start()
        threads.append(dht1_thread)
        print("Dht2 loop started")
