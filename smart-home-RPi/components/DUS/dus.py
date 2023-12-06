from simulators.DUS.dus import run_uds_simulator
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

def dus_callback(distance, print_lock, settings, publish_event):
    global publish_data_counter, publish_data_limit

    with print_lock:
        t = time.localtime()
        print("=" * 20)
        print(f"UDS: {settings['name']}")
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f'Distance: {distance} cm')

    distance_payload = {
        "measurement": "Distance",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": distance
    }

    with counter_lock:
        dht_batch.append(('Distance', json.dumps(distance_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_dus(settings, threads, stop_event, print_lock):
    if settings['simulated']:
        dus_thread = threading.Thread(target=run_uds_simulator,
                                      args=(2, dus_callback, stop_event, print_lock, settings, publish_event))
        dus_thread.start()
        threads.append(dus_thread)
    else:
        from sensors.DUS.DUS import run_dus_loop
        dus_thread = threading.Thread(target=run_dus_loop,
                                      args=(2, dus_callback, stop_event, print_lock, settings, publish_event))
        dus_thread.start()
        threads.append(dus_thread)

