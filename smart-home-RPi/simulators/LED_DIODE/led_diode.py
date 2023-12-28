import time
from sensors.LED_DIODE.DL import DL


def toggle_door_light(dl, dl_callback, print_lock, settings, publish_event):

    dl.turn_on_sim()
    dl_callback(dl.state, print_lock, settings, publish_event)
    time.sleep(10)
    dl_callback(dl.state, print_lock, settings, publish_event)

    dl.turn_off_sim()
    dl_callback(dl.state, print_lock, settings, publish_event)


def run_dl_simulator(dl_callback, stop_event, print_lock, settings, publish_event, light_event):
    dl = DL(settings['pin'])
    while not stop_event.is_set():
        light_event.wait()
        toggle_door_light(dl, dl_callback, print_lock, settings, publish_event)
        light_event.clear()


