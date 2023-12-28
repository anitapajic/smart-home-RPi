import threading
from datetime import datetime

from simulators.BUZZ.buzz import listen_for_keypress
from sensors.BUZZ.DB import db_loop
from sensors.BUZZ.BB import bb_loop
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT

buzz_batch = []
publish_data_counter = 0
publish_data_limit = 3
counter_lock = threading.Lock()


def publisher_task(event, buzz_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_pir_batch = buzz_batch.copy()
            publish_data_counter = 0
            buzz_batch.clear()
        publish.multiple(local_pir_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} buzzer values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, buzz_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def buzz_callback(settings, publish_event, isOn):
    global publish_data_counter, publish_data_limit

    current_time = datetime.utcnow().isoformat()  # Convert current time to ISO 8601 string format

    movement_payload = {
        "measurement": "Buzzers",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": isOn,
        "timestamp": current_time
    }

    with counter_lock:
        buzz_batch.append(('Buzzers', json.dumps(movement_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_db1(settings, threads, stop_event, print_lock, alarm):
    pitch = settings.get('pitch', 440)  # Default to 440 if not set
    duration = settings.get('duration', 1000)  # Default to 1 if not set

    if settings['simulated']:
        buzzer_thread = threading.Thread(target=listen_for_keypress, args=(stop_event, print_lock, pitch, duration, settings, publish_event, buzz_callback, alarm))
        buzzer_thread.start()
        threads.append(buzzer_thread)
    else:
        buzzer_pin = settings['pin']
        buzzer_thread = threading.Thread(target=db_loop, args=(buzzer_pin, 440, 1, settings, publish_event, buzz_callback, alarm))
        buzzer_thread.start()
        threads.append(buzzer_thread)


def run_bb(settings, threads, stop_event, print_lock):
    pitch = settings.get('pitch', 440)  # Default to 440 if not set
    duration = settings.get('duration', 1000)  # Default to 1 if not set

    if settings['simulated']:
        buzzer_thread = threading.Thread(target=listen_for_keypress, args=(stop_event, print_lock, pitch, duration, settings, publish_event, buzz_callback))
        buzzer_thread.start()
        threads.append(buzzer_thread)
    else:
        print("Starting real buzzer")
        buzzer_pin = settings['pin']
        buzzer_thread = threading.Thread(target=bb_loop, args=(buzzer_pin, 440, 1, settings, publish_event, buzz_callback))
        buzzer_thread.start()
        threads.append(buzzer_thread)
        print("Real buzzer started")

