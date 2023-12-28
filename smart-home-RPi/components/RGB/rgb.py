import threading
from datetime import datetime
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
from simulators.RGB.rgb import simulated_rgb


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
        print(f'published {publish_data_limit} rgb values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, rgb_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def rgb_callback(rgb_settings, publish_event, color):
    global publish_data_counter, publish_data_limit

    current_time = datetime.utcnow().isoformat()
    color_payload = {
        "measurement": "RGB",
        "simulated": rgb_settings['simulated'],
        "runs_on": rgb_settings["runs_on"],
        "name": rgb_settings["name"],
        "value": color,
        "timestamp": current_time
    }

    with counter_lock:
        rgb_batch.append(('RGB', json.dumps(color_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_rgb(print_lock, stop_event, threads, rgb_settings, rgb_queue):
    if rgb_settings['simulated']:
        rgb_thread = threading.Thread(target=simulated_rgb,
                                      args=(rgb_settings['name'], print_lock, stop_event, rgb_settings, publish_event,
                                            rgb_callback, rgb_queue))
        rgb_thread.start()
        threads.append(rgb_thread)
    else:
        from sensors.RGB.BRGB import rgb_loop
        rgb_thread = threading.Thread(target=rgb_loop,
                                      args=(rgb_settings['red_pin'], rgb_settings['green_pin'], rgb_settings['blue_pin']
                                            , stop_event, rgb_settings, publish_event, rgb_callback, print_lock,
                                            rgb_queue))
        rgb_thread.start()
        threads.append(rgb_thread)
