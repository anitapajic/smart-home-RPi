import sys
import threading
import time
#from pynput import keyboard
import keyboard
import json
from datetime import datetime
from settings import load_settings
from components.DHT.dht import run_dht
from components.BUTTON.ds import run_ds
from components.DUS.dus import run_dus
from components.MS.ms import run_keypad
from components.PIR.pir import run_RPIR1, run_RPIR2, run_DPIR1, run_RPIR4, run_DPIR2, run_RPIR3
from components.GYRO.gyro import run_gyro
from components.LCD.lcd import run_lcd
from components.IR.ir import run_BIR
from components.B4SD.b4sd import run_b4sd
from components.LED_DIODE.led_diode import run_dl
from components.RGB.rgb import run_rgb
from components.BUZZ.buzz import run_db1, run_bb
from queue import Queue
from home import Home
from mqtt import listen_for_mqtt, mqtt, on_message, on_connect
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT


print_lock = threading.Lock()
light_event = threading.Event()
dus1_event = threading.Event()
dus2_event = threading.Event()
alarm_event = threading.Event()
ds_event = threading.Event()
switch1_event = threading.Event()
switch2_event = threading.Event()
switch_off2 = threading.Event()
switch_off1 = threading.Event()
gdht_queue = Queue()
rgb_queue = Queue()
alarm_clock_event = threading.Event()


try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass


# def on_press(key, switch, target_key):
#     if hasattr(key, 'char') and key.char == target_key:
#         if not switch.is_set():
#             print("pressed")
#             switch.set()
#
#
#
# def on_release(key, switch_off, target_key):
#     if hasattr(key, 'char') and key.char == target_key:
#         if not switch_off.is_set():
#             print("released")
#             switch_off.set()
#
#
# def ds_button_simulator(switch, switch_off, name, target_key):
#     # Create a keyboard listener
#     with keyboard.Listener(
#         on_press=lambda key: on_press(key, switch, target_key),
#         on_release=lambda key: on_release(key, switch_off, target_key)
#     ) as listener:
#         listener.join()

def ds_button_simulator(switch, switch_off, name, key):
    while True:
        if not switch.is_set():
            keyboard.wait(key)
            switch.set()
        if not switch_off.is_set():
            keyboard.wait(key, suppress=True, trigger_on_release=True)
            switch_off.set()


test_batch = []


def test_alarm(home, event):
    while True:
        event.wait()
        home.alarm = True
        test_batch.append(('alarm', json.dumps({"a": "a"}), 0, True))
        publish.multiple(test_batch, hostname=HOSTNAME, port=PORT)
        time.sleep(2)


clock_batch = []


def check_alarm(home, alarm_clock_event):
    while True:
        if home.alarm_clock:
            alarm_time = datetime.strptime(home.alarm_clock, "%Y-%m-%dT%H:%M")
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%dT%H:%M")
            formatted_time = datetime.strptime(formatted_time, "%Y-%m-%dT%H:%M")
            print(formatted_time, alarm_time)
            if formatted_time == alarm_time:
                alarm_clock_event.set()
                clock_batch.append(('clock', json.dumps({"a": "a"}), 0, True))
                publish.multiple(clock_batch, hostname=HOSTNAME, port=PORT)
                time.sleep(2)
        time.sleep(1)


def run_simulators(stop_event):

    # STOP
    home = Home("1111#")

    enter_thread = threading.Thread(target=listen_for_stop_command, args=(stop_event,))
    enter_thread.start()

    mqtt_thread = threading.Thread(target=listen_for_mqtt, args=(mqtt, on_connect, on_message, home, alarm_event,
                                                                 alarm_clock_event))
    mqtt_thread.start()

    mqtth_thread = threading.Thread(target=test_alarm, args=(home, alarm_event))
    mqtth_thread.start()

    clock_thread = threading.Thread(target=check_alarm, args=(home, alarm_clock_event))
    clock_thread.start()

    enter1_thread = threading.Thread(target=ds_button_simulator, args=(switch1_event, switch_off1, '1', 'm'))
    enter1_thread.start()

    enter2_thread = threading.Thread(target=ds_button_simulator, args=(switch2_event, switch_off2, '2', 'n'))
    enter2_thread.start()

    # DHT
    dht1_settings = settings['DHT1']
    run_dht(dht1_settings, threads, stop_event, print_lock)

    dht2_settings = settings['DHT2']
    run_dht(dht2_settings, threads, stop_event, print_lock)

    dht3_settings = settings['DHT3']
    run_dht(dht3_settings, threads, stop_event, print_lock)

    dht4_settings = settings['DHT4']
    run_dht(dht4_settings, threads, stop_event, print_lock)

    gdht_settings = settings['GDHT']
    run_dht(gdht_settings, threads, stop_event, print_lock, gdht_queue)

    # PIR
    rpir1_settings = settings['RPIR1']
    run_RPIR1(rpir1_settings, threads, stop_event, print_lock, home, alarm_event)

    rpir2_settings = settings['RPIR2']
    run_RPIR2(rpir2_settings, threads, stop_event, print_lock, home, alarm_event)

    rpir3_settings = settings['RPIR3']
    run_RPIR3(rpir3_settings, threads, stop_event, print_lock, home, alarm_event)

    rpir4_settings = settings['RPIR4']
    run_RPIR4(rpir4_settings, threads, stop_event, print_lock, home, alarm_event)

    dpir1_settings = settings['DPIR1']
    run_DPIR1(dpir1_settings, threads, stop_event, print_lock, home, dus1_event, light_event)

    dpir2_settings = settings['DPIR2']
    run_DPIR2(dpir2_settings, threads, stop_event, print_lock, home, dus2_event)

    # DL
    dl_settings = settings['DL']
    run_dl(dl_settings, threads, stop_event, print_lock, light_event)

    # DS
    ds1_settings = settings['DS1']
    run_ds(ds1_settings, threads, stop_event, print_lock, alarm_event, switch1_event, ds_event, home, switch_off1)

    ds2_settings = settings['DS2']
    run_ds(ds2_settings, threads, stop_event, print_lock, alarm_event, switch2_event, ds_event, home, switch_off2)

    # DUS
    dus1_settings = settings['DUS1']
    run_dus(dus1_settings, threads, stop_event, print_lock, home, dus1_event)

    dus2_settings = settings['DUS2']
    run_dus(dus2_settings, threads, stop_event, print_lock, home, dus2_event)

    # MS
    dms1_settings = settings['DMS1']
    run_keypad(dms1_settings, threads, stop_event, print_lock, home, alarm_event, ds_event)

    # GYRO
    grg_settings = settings['GRG']
    run_gyro(grg_settings, threads, stop_event, print_lock, alarm_event)

    # LCD
    glcd_settings = settings["GLCD"]
    run_lcd(glcd_settings, threads, stop_event, print_lock, gdht_queue)

    # B4SD
    b4sd_settings = settings["B4SD"]
    run_b4sd(b4sd_settings, threads, stop_event, print_lock, alarm_event)

    # Buzzer
    db1_settings = settings['DB1']
    run_db1(db1_settings, threads, stop_event, print_lock, alarm_event, alarm_clock_event)

    db1_settings = settings['BB']
    run_bb(db1_settings, threads, stop_event, print_lock, alarm_event, alarm_clock_event)

    # RGB
    rgb_settings = settings['BRGB']
    run_rgb(print_lock, stop_event, threads, rgb_settings, rgb_queue)

    # BIR
    bir_settings = settings['BIR']
    run_BIR(bir_settings, threads, stop_event, print_lock, rgb_queue)

    for thread in threads:
        thread.join()


def listen_for_stop_command(stop_event):
    command = input("Press '0' to stop all simulations...\n")
    if command == '0':
        for t in threads:
            stop_event.set()
        sys.exit(0)


if __name__ == "__main__":
    print('Starting app')
    settings = load_settings()
    threads = []
    stop_event = threading.Event()
    try:
        run_simulators(stop_event)
        stop_event.clear()
        threads = []

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()
