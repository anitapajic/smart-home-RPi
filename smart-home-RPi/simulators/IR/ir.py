import time
import random
import threading
from simulators.RGB.rgb import simulated_rgb
from sensors.RGB.BRGB import rgb_loop


def simulated_ir(threads, print_lock, stop_event, settings, publish_event, ir_callback, rgb_publish_event, rgb_callback):
    while True:
        if stop_event.is_set():
            break
        ButtonsNames = ["LEFT", "RIGHT", "UP", "DOWN", "2", "3", "1", "OK", "4", "5", "6", "7", "8", "9", "*", "0",
                        "#"]  # String list in same order as HEX list
        button = random.choice(list(ButtonsNames))
        if settings['BRGB']['simulated']:
            rgb_thread = threading.Thread(target=simulated_rgb, args=(settings['BRGB']['name'], print_lock,
                                                                      stop_event, settings['BRGB'], rgb_publish_event,
                                                                      rgb_callback, ButtonsNames[button]))
            rgb_thread.start()
            threads.append(rgb_thread)
        else:
            rgb_loop(settings['BRGB']['red_pin'], settings['BRGB']['green_pin'], settings['BRGB']['blue_pin'],
                     stop_event, settings['BRGB'], rgb_publish_event, rgb_callback, ButtonsNames[button], print_lock)

        ir_callback(settings['BIR']['name'], print_lock, stop_event, settings['BIR'], publish_event,
                     ButtonsNames[button])

        time.sleep(2)