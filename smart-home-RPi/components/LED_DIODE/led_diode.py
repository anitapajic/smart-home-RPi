from  simulators.LED_DIODE.led_diode import run_dl_simulator
import threading
import time
from datetime import datetime
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT

dht_batch = []
publish_data_counter = 0
publish_data_limit = 1
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
        print(f'published {publish_data_limit} dl values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def dl_callback(state, print_lock, settings, publish_event):
    global publish_data_counter, publish_data_limit

    with print_lock:
        t = time.localtime()
        print("=" * 20)
        print(f"{settings['name']}")
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"State: {int(state)}")

    current_time = datetime.utcnow().isoformat()

    dl_payload = {
        "measurement": "Door light 1",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": int(state),
        "timestamp": current_time

    }

    with counter_lock:
        dht_batch.append(('LED', json.dumps(dl_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_dl(settings, threads, stop_event, print_lock, light_event):
    if settings['simulated']:
        dl_thread = threading.Thread(target=run_dl_simulator,
                                     args=(dl_callback, stop_event, print_lock, settings, publish_event, light_event))
        dl_thread.start()
        threads.append(dl_thread)
    else:
        from sensors.LED_DIODE.DL import run_dl_loop
        dl_thread = threading.Thread(target=run_dl_loop,
                                     args=(dl_callback, stop_event, print_lock, settings, publish_event, light_event))
        dl_thread.start()
        threads.append(dl_thread)

