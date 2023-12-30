from simulators.BUTTON.ds import run_ds_simulator
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
        print(f'published {publish_data_limit} ds values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def dl_callback(state, print_lock, settings, publish_event):
    global publish_data_counter, publish_data_limit

    # with print_lock:
    #     t = time.localtime()
    #     print("=" * 20)
    #     print(f"{settings['name']}")
    #     print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    #     print(f"State: {state}")

    current_time = datetime.utcnow().isoformat()

    dl_payload = {
        "measurement": "Door Sensor",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": state,
        "timestamp": current_time

    }

    with counter_lock:
        dht_batch.append(('Buttons', json.dumps(dl_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()




def run_ds(settings, threads, stop_event, print_lock, alarm_ds, switch, ds_event, home, switch_off):
    if settings['simulated']:
        dl_thread = threading.Thread(target=run_ds_simulator, args=(dl_callback, stop_event, print_lock, settings, publish_event, alarm_ds, switch, ds_event, home, switch_off))
        dl_thread.start()
        threads.append(dl_thread)
    else:
        from sensors.BUTTON.DS import run_ds_loop
        dl_thread = threading.Thread(target=run_ds_loop, args=(dl_callback, stop_event, print_lock, settings, publish_event, alarm_ds, switch, ds_event, home))
        dl_thread.start()
        threads.append(dl_thread)