import random
import time


button_to_color_name = {
    "1": "red",
    "2": "green",
    "3": "blue",
    "4": "yellow",
    "5": "white",
    "6": "purple",
    "7": "lightBlue",
    # Dodajte ostale taster-boja mapiranja
}


def simulated_rgb(rgb_name, print_lock, stop_event, settings, publish_event, rgb_callback, taster):
    while True:
        if stop_event.is_set():
            break
        if taster in button_to_color_name:
            current_color_name = button_to_color_name[taster]
            rgb_callback(rgb_name, print_lock, stop_event, settings, publish_event, current_color_name)
        else:
            with print_lock:
                print("No color is shown on ", rgb_name)
        time.sleep(3)
