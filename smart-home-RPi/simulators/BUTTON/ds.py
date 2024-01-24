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


def run_ds_simulator(ds_callback, stop_event, print_lock, settings, publish_event, alarm_ds, switch, ds_event, home,
                     switch_off):
    ds = DS(settings['pin'])
    while True:
        switch.wait()
        switch_off.clear()
        toggle_door_sensor(ds, ds_callback, print_lock, settings, publish_event, alarm_ds)
        if home.safety_system and ds.state:
            ds_event.set()  # unesi pin, ako ne uneses ispravan za 10s krece alarm
        while switch.is_set():
            if time.time() - ds.time > 5:  # ds.time je timestamp kad se ukljucio
                alarm_ds.set()
                home.alarm = True
            if switch_off.is_set():
                toggle_door_sensor(ds, ds_callback, print_lock, settings, publish_event, alarm_ds)
                switch.clear()
                alarm_ds.clear()
                home.alarm = False
                break

        if stop_event.is_set():
            ds.turn_off_sim()  # Ensure the light is off when stopping
            ds_callback(False, print_lock, settings, publish_event)
            alarm_ds.clear()
            break
