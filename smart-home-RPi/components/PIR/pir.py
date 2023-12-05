import threading
from simulators.PIR.pir import simulated_pir
import time
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT


pir_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, pir_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_pir_batch = pir_batch.copy()
            publish_data_counter = 0
            pir_batch.clear()
        publish.multiple(local_pir_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} pir values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, pir_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def pir_callback(name, print_lock, stop_event, dht_settings, publish_event, movement):
    global publish_data_counter, publish_data_limit

    movement_payload = {
        "measurement": "Pirs",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "value": movement
    }

    with counter_lock:
        pir_batch.append(('Pirs', json.dumps(movement_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_RPIR1(settings, threads, stop_event, print_lock):

    pir_name = settings['name']

    if settings['simulated']:
        pir_thread = threading.Thread(target=simulated_pir, args=(pir_name, print_lock, stop_event, settings, publish_event, pir_callback))
        pir_thread.start()
        threads.append(pir_thread)
    else:
        from sensors.PIR.RPIR1 import real_pir
        pin = settings['pin']
        pir_thread = threading.Thread(target=real_pir, args=pin)
        pir_thread.start()
        threads.append(pir_thread)


def run_RPIR2(settings, threads, stop_event, print_lock):

    pir_name = settings['name']

    if settings['simulated']:
        pir_thread = threading.Thread(target=simulated_pir, args=(pir_name, print_lock, stop_event, settings, publish_event, pir_callback))
        pir_thread.start()
        threads.append(pir_thread)
    else:
        from sensors.PIR.RPIR2 import real_pir
        pin = settings['pin']
        pir_thread = threading.Thread(target=real_pir, args=pin)
        pir_thread.start()
        threads.append(pir_thread)


def run_DPIR1(settings, threads, stop_event, print_lock):
    pir_name = settings['name']

    if settings['simulated']:
        pir_thread = threading.Thread(target=simulated_pir, args=(pir_name, print_lock, stop_event, settings, publish_event, pir_callback))
        pir_thread.start()
        threads.append(pir_thread)
    else:
        from sensors.PIR.DPIR1 import real_pir
        pin = settings['pin']
        pir_thread = threading.Thread(target=real_pir, args=pin)
        pir_thread.start()
        threads.append(pir_thread)


# def run_DS1(settings, threads, stop_event, print_lock):
#     pir_name = settings['name']
#
#     if settings['simulated']:
#         pir_thread = threading.Thread(target=simulated_pir, args=(pir_name, print_lock, stop_event))
#         pir_thread.start()
#         threads.append(pir_thread)
#     else:
#         from sensors.PIR.DS1 import real_pir
#         pin = settings['pin']
#         pir_thread = threading.Thread(target=real_pir, args=pin)
#         pir_thread.start()
#         threads.append(pir_thread)