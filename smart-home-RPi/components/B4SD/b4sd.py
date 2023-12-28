from simulators.B4SD.b4sd import run_b4sd_simulator
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
        print(f'published {publish_data_limit} b4sd values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def b4sd_callback(message, print_lock, settings, publish_event):
    global publish_data_counter, publish_data_limit

    with print_lock:
        t = time.localtime()
        print("=" * 20)
        print(f"B2SD: {settings['name']}")
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f'Message: {message}')
    current_time = datetime.utcnow().isoformat()

    b4sd_payload = {
        "measurement": "B4SD",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": message,
        "timestamp": current_time
    }

    with counter_lock:
        dht_batch.append(('B4SD', json.dumps(b4sd_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_b4sd(settings, threads, stop_event, print_lock):
    if settings['simulated']:
        b4sd_thread = threading.Thread(target=run_b4sd_simulator,
                                      args=(b4sd_callback, stop_event, print_lock, settings, publish_event))
        b4sd_thread.start()
        threads.append(b4sd_thread)
    else:
        from sensors.B4SD.B4SD import run_b4sd_loop
        b4sd_thread = threading.Thread(target=run_b4sd_loop,
                                      args=(b4sd_callback, stop_event, print_lock, settings, publish_event))
        b4sd_thread.start()
        threads.append(b4sd_thread)

