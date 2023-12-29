import threading
from simulators.MS.ms import simulated_keypad
from sensors.MS.DMS1 import real_keypad
from datetime import datetime
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT


ms_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, ms_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_ms_batch = ms_batch.copy()
            publish_data_counter = 0
            ms_batch.clear()
        publish.multiple(local_ms_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} ms values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, ms_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def ms_callback(print_lock, stop_event, ms_settings, publish_event, code):
    global publish_data_counter, publish_data_limit

    current_time = datetime.utcnow().isoformat()

    code_payload = {
        "measurement": "Keypads",
        "simulated": ms_settings['simulated'],
        "runs_on": ms_settings["runs_on"],
        "name": ms_settings["name"],
        "value": code,
        "timestamp": current_time
    }

    with counter_lock:
        ms_batch.append(('Keypads', json.dumps(code_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_keypad(settings, threads, stop_event, print_lock, home, alarm, ds_event):
    if settings['simulated']:
        keypad_thread = threading.Thread(target=simulated_keypad, args=(print_lock, stop_event, settings, publish_event, ms_callback, home, alarm, ds_event))
        keypad_thread.start()
        threads.append(keypad_thread)
    else:
        print("Starting real keypad")
        keypad_thread = threading.Thread(target=real_keypad, args=(print_lock, stop_event, settings, publish_event, ms_callback, home, alarm, ds_event))
        keypad_thread.start()
        threads.append(keypad_thread)