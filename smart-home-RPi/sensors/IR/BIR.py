# -----------------------------------------#
# Name - IR-Finalized.py
# Description - The finalized code to read data from an IR sensor and then reference it with stored values
# Author - Lime Parallelogram
# License - Completely Free
# Date - 12/09/2019
# ------------------------------------------------------------#
# Imports modules
try:
    import RPi.GPIO as GPIO
except:
    pass
import threading
from datetime import datetime
import time
from sensors.RGB.BRGB import rgb_loop
from simulators.RGB.rgb import simulated_rgb

# Static program vars

Buttons = [0x300ff22dd, 0x300ffc23d, 0x300ff629d, 0x300ffa857, 0x300ff9867, 0x300ffb04f, 0x300ff6897, 0x300ff02fd,
           0x300ff30cf, 0x300ff18e7, 0x300ff7a85, 0x300ff10ef, 0x300ff38c7, 0x300ff5aa5, 0x300ff42bd, 0x300ff4ab5,
           0x300ff52ad]  # HEX code list
ButtonsNames = ["LEFT", "RIGHT", "UP", "DOWN", "2", "3", "1", "OK", "4", "5", "6", "7", "8", "9", "*", "0",
                "#"]  # String list in same order as HEX list

# Sets up GPIO
def setup(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN)


# Gets binary value


def getBinary(pin):
    # Internal vars
    num1s = 0  # Number of consecutive 1s read
    binary = 1  # The binary value
    command = []  # The list to store pulse times in
    previousValue = 0  # The last value
    value = GPIO.input(pin)  # The current value

    # Waits for the sensor to pull pin low
    while value:
        time.sleep(0.0001)  # This sleep decreases CPU utilization immensely
        value = GPIO.input(pin)

    # Records start time
    startTime = datetime.now()

    while True:
        # If change detected in value
        if previousValue != value:
            now = datetime.now()
            pulseTime = now - startTime  # Calculate the time of pulse
            startTime = now  # Reset start time
            command.append((previousValue, pulseTime.microseconds))  # Store recorded data

        # Updates consecutive 1s variable
        if value:
            num1s += 1
        else:
            num1s = 0

        # Breaks program when the amount of 1s surpasses 10000
        if num1s > 10000:
            break

        # Re-reads pin
        previousValue = value
        value = GPIO.input(pin)

    # Converts times to binary
    for (typ, tme) in command:
        if typ == 1:  # If looking at rest period
            if tme > 1000:  # If pulse greater than 1000us
                binary = binary * 10 + 1  # Must be 1
            else:
                binary *= 10  # Must be 0

    if len(str(binary)) > 34:  # Sometimes, there is some stray characters
        binary = int(str(binary)[:34])

    return binary


# Convert value to hex
def convertHex(binaryValue):
    tmpB2 = int(str(binaryValue), 2)  # Temporarely propper base 2
    return hex(tmpB2)


def bir_loop(threads, print_lock, stop_event, settings, rgb_publish_event, publish_event, rgb_callback, bir_callback):
    try:
        setup(settings['BIR']['pin'])
        while not stop_event.is_set():
            inData = convertHex(getBinary(settings['BIR']['pin']))  # Runs subs to get incoming hex value
            print(inData)
            for button in range(len(Buttons)):  # Runs through every value in list
                if hex(Buttons[button]) == inData:  # Checks this against incoming
                    # print(ButtonsNames[button])  # Prints corresponding english name for button
                    if settings['BRGB']['simulated']:
                        rgb_thread = threading.Thread(target=simulated_rgb, args=(settings['BRGB']['name'], print_lock,
                                                                                  stop_event, settings['BRGB'], rgb_publish_event, rgb_callback, ButtonsNames[button]))
                        rgb_thread.start()
                        threads.append(rgb_thread)
                    else:
                        rgb_loop(settings['BRGB']['red_pin'], settings['BRGB']['green_pin'], settings['BRGB']['blue_pin'],
                                 stop_event, settings['BRGB'], rgb_publish_event, rgb_callback, ButtonsNames[button], print_lock)

                    bir_callback(settings['BIR']['name'], print_lock, stop_event, settings['BIR'], publish_event,
                                 ButtonsNames[button])
    except KeyboardInterrupt:
        print("\nBIR sensor stopped!")
    finally:
        GPIO.cleanup()
