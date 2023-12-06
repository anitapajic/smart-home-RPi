from simulators.DHT.dht import run_dht_simulator
import threading
import time
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT



dht_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, dht_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dht_batch = dht_batch.copy()
            publish_data_counter = 0
            dht_batch.clear()
        publish.multiple(local_dht_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} dht values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def dht_callback(humidity, temperature, code, print_lock, dht_settings, publish_event):
    global publish_data_counter, publish_data_limit

    # with print_lock:
    #     t = time.localtime()
    #     print("=" * 20)
    #     print(f"DHT: {dht_settings['name']}")
    #     print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    #     print(f"Code: {code}")
    #     print(f"Humidity: {humidity}%")
    #     print(f"Temperature: {temperature}°C")

    temp_payload = {
        "measurement": "Temperature",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "value": temperature
    }

    humidity_payload = {
        "measurement": "Humidity",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "value": humidity
    }
    with counter_lock:
        dht_batch.append(('Temperature', json.dumps(temp_payload), 0, True))
        dht_batch.append(('Humidity', json.dumps(humidity_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_dht1(settings, threads, stop_event, print_lock):
    dht = settings['name']
    if settings['simulated']:
        dht1_thread = threading.Thread(target=run_dht_simulator, args=(2, dht_callback, stop_event, print_lock, settings, publish_event))
        dht1_thread.start()
        threads.append(dht1_thread)
    else:
        from sensors.DHT.RDHT1 import run_dht_loop, DHT
        print("Starting dht1 loop")
        dht = DHT(settings['pin'])
        dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, dht_callback, stop_event, print_lock, dht, publish_event))
        dht1_thread.start()
        threads.append(dht1_thread)
        print("Dht1 loop started")


def run_dht2(settings, threads, stop_event, print_lock):
    dht_name = settings['name']
    if settings['simulated']:
        dht1_thread = threading.Thread(target=run_dht_simulator, args=(2, dht_callback, stop_event, print_lock, settings, publish_event))
        dht1_thread.start()
        threads.append(dht1_thread)
    else:
        from sensors.DHT.RDHT2 import run_dht_loop, DHT
        print("Starting dht2 loop")
        dht = DHT(settings['pin'])
        dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, dht_callback, stop_event, print_lock, dht_name, publish_event))
        dht1_thread.start()
        threads.append(dht1_thread)
        print("Dht2 loop started")
