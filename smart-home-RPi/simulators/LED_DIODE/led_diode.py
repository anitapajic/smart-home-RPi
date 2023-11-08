
import keyboard
import time


def toggle_door_light(dl, dl_callback, print_lock, dl_name):
    dl.toggle()
    if dl.state:
        dl.turnOn()
        dl_callback("Door Light is ON", print_lock, dl_name)
    else:
        dl.turnOff()
        dl_callback("Door Light is OFF", print_lock, dl_name)

def run_dl_simulator(dl, dl_callback, stop_event, print_lock, dl_name):
    while not stop_event.is_set():
        if keyboard.is_pressed('m'):
            toggle_door_light(dl, dl_callback, print_lock, dl_name)
            time.sleep(0.2)  # Debounce to prevent rapid toggling
        time.sleep(0.01)  # Adjust sleep time as needed for responsiveness
