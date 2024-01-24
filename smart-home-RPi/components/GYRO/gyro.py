import threading
from datetime import datetime
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
from simulators.GYRO.gyro import simulated_gyro


gyro_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, gyro_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_pir_batch = gyro_batch.copy()
            publish_data_counter = 0
            gyro_batch.clear()
        publish.multiple(local_pir_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} gyro values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, gyro_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def gyro_callback(settings, publish_event, gyro, accel):
    global publish_data_counter, publish_data_limit

    current_time = datetime.utcnow().isoformat()
    gyro_payload = {
        "measurement": "Gyroscope",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": gyro,
        "timestamp": current_time
    }
    accel_payload = {
        "measurement": "Accelerometer",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": accel,
        "timestamp": current_time
    }

    with counter_lock:
        gyro_batch.append(('Gyroscope', json.dumps(gyro_payload), 0, True))
        gyro_batch.append(('Gyroscope', json.dumps(accel_payload), 0, True))

        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_gyro(settings, threads, stop_event, print_lock, alarm_event):
    if settings['simulated']:
        gyro_thread = threading.Thread(target=simulated_gyro,
                                       args=(print_lock, stop_event, settings, publish_event, gyro_callback,
                                             alarm_event))
        gyro_thread.start()
        threads.append(gyro_thread)
    else:
        from sensors.GYRO.GRG import run_gyro_loop
        gyro_thread = threading.Thread(target=run_gyro_loop,
                                       args=(print_lock, stop_event, settings, publish_event, gyro_callback,
                                             alarm_event))
        gyro_thread.start()
        threads.append(gyro_thread)
