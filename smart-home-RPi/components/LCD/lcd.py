from simulators.LCD.lcd import run_lcd_simulator
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
        print(f'published {publish_data_limit} lcd values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def lcd_callback(message, print_lock, settings, publish_event):
    global publish_data_counter, publish_data_limit

    with print_lock:
        t = time.localtime()
        print("=" * 20)
        print(f"LCD: {settings['name']}")
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f'Message: {message}')
    current_time = datetime.utcnow().isoformat()

    lcd_payload = {
        "measurement": "LCD",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": message,
        "timestamp": current_time
    }

    with counter_lock:
        dht_batch.append(('LCD', json.dumps(lcd_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_lcd(settings, threads, stop_event, print_lock, queue):
    if settings['simulated']:
        lcd_thread = threading.Thread(target=run_lcd_simulator,
                                      args=(lcd_callback, stop_event, print_lock, settings, publish_event, queue))
        lcd_thread.start()
        threads.append(lcd_thread)
    else:
        from sensors.LCD.GLCD import run_lcd_loop
        lcd_thread = threading.Thread(target=run_lcd_loop,
                                      args=(lcd_callback, stop_event, print_lock, settings, publish_event, queue))
        lcd_thread.start()
        threads.append(lcd_thread)

