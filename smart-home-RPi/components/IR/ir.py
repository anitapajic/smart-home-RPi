import threading
from datetime import datetime
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
from components.RGB.rgb import publish_event, rgb_callback
from simulators.IR.ir import simulated_ir

rgb_publish_event = publish_event
rgb_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, rgb_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_rgb_batch = rgb_batch.copy()
            publish_data_counter = 0
            rgb_batch.clear()
        publish.multiple(local_rgb_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} bir values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, rgb_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def bir_callback(name, print_lock, stop_event, rgb_settings, publish_event, taster):
    global publish_data_counter, publish_data_limit

    current_time = datetime.utcnow().isoformat()
    color_payload = {
        "measurement": "IR",
        "simulated": rgb_settings['simulated'],
        "runs_on": rgb_settings["runs_on"],
        "name": rgb_settings["name"],
        "value": taster,
        "timestamp": current_time
    }

    with counter_lock:
        rgb_batch.append(('IR', json.dumps(color_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_BIR(settings, threads, stop_event, print_lock):
    if settings['BIR']['simulated']:
        rgb_thread = threading.Thread(target=simulated_ir, args=(threads, print_lock, stop_event, settings, publish_event, bir_callback, rgb_publish_event, rgb_callback))
        rgb_thread.start()
        threads.append(rgb_thread)
    else:
        from sensors.IR.BIR import bir_loop
        rgb_thread = threading.Thread(target=bir_loop, args=(threads, print_lock, stop_event, settings, rgb_publish_event, publish_event, rgb_callback, bir_callback))
        rgb_thread.start()
        threads.append(rgb_thread)
