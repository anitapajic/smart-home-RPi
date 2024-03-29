from simulators.DHT.dht import run_dht_simulator
import threading
import time
from datetime import datetime
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


def dht_callback(humidity, temperature, code, print_lock, settings, publish_event):
    global publish_data_counter, publish_data_limit

    with print_lock:
        t = time.localtime()
        print("=" * 20)
        print(f"DHT: {settings['name']}")
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Humidity: {humidity}%")
        print(f"Temperature: {temperature}°C")

    current_time = datetime.utcnow().isoformat()

    temp_payload = {
        "measurement": "Temperature",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": temperature,
        "timestamp": current_time
    }

    current_time = datetime.utcnow().isoformat()

    humidity_payload = {
        "measurement": "Humidity",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": humidity,
        "timestamp": current_time
    }
    with counter_lock:
        dht_batch.append(('Temperature', json.dumps(temp_payload), 0, True))
        dht_batch.append(('Humidity', json.dumps(humidity_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_dht(settings, threads, stop_event, print_lock, queue=None):
    if settings['simulated']:
        dht_thread = threading.Thread(target=run_dht_simulator,
                                      args=(5, dht_callback, stop_event, print_lock, settings, publish_event, queue))
        dht_thread.start()
        threads.append(dht_thread)
    else:
        from sensors.DHT.DHT import run_dht_loop
        dht_thread = threading.Thread(target=run_dht_loop,
                                      args=(5, dht_callback, stop_event, print_lock, settings, publish_event, queue))
        dht_thread.start()
        threads.append(dht_thread)
