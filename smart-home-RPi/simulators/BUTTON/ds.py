import random

import keyboard
import time
from sensors.BUTTON.DS import DS


def toggle_door_sensor(ds, ds_callback, print_lock, settings, publish_event, alarm_ds):
    if ds.state:
        ds.turn_off_sim()
        # if alarm_ds.is_set():
            # alarm_ds.clear()
            # print("Ugasen alarm")

    else:
        ds.turn_on_sim()

    ds_callback(ds.state, print_lock, settings, publish_event)

def run_ds_simulator(ds_callback, stop_event, print_lock, settings, publish_event, alarm_ds, switch, ds_event, home):
    ds = DS(settings['pin'])
    while True:
        switch.wait()
        toggle_door_sensor(ds, ds_callback, print_lock, settings, publish_event, alarm_ds)

        if home.safety_system and ds.state:
            ds_event.set() #unesi pin, ako ne uneses ispravan za 10s krece alarm

        time.sleep(random.randint(0, 7))
        if time.time() - ds.time > 5:
            alarm_ds.set()
            home.alarm = True
            print("Otkljucana duze od 5s : ", settings['name'])

        switch.clear()

        if stop_event.is_set():
            ds.turn_off_sim()  # Ensure the light is off when stopping
            ds_callback(False, print_lock, settings, publish_event)
            alarm_ds.clear()
            break
