import time

try:
    import RPi.GPIO as GPIO
except:
    pass
from time import sleep


def setup(RED_PIN, GREEN_PIN, BLUE_PIN):
    # disable warnings (optional)
    GPIO.setwarnings(False)

    GPIO.setmode(GPIO.BCM)
    # set pins as outputs
    GPIO.setup(RED_PIN, GPIO.OUT)
    GPIO.setup(GREEN_PIN, GPIO.OUT)
    GPIO.setup(BLUE_PIN, GPIO.OUT)



def turnOff(RED_PIN, GREEN_PIN, BLUE_PIN):
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.LOW)


def white(RED_PIN, GREEN_PIN, BLUE_PIN):
    GPIO.output(RED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(BLUE_PIN, GPIO.HIGH)


def red(RED_PIN, GREEN_PIN, BLUE_PIN):
    GPIO.output(RED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.LOW)


def green(RED_PIN, GREEN_PIN, BLUE_PIN):
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(BLUE_PIN, GPIO.LOW)


def blue(RED_PIN, GREEN_PIN, BLUE_PIN):
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.HIGH)


def yellow(RED_PIN, GREEN_PIN, BLUE_PIN):
    GPIO.output(RED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(BLUE_PIN, GPIO.LOW)


def purple(RED_PIN, GREEN_PIN, BLUE_PIN):
    GPIO.output(RED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.HIGH)


def lightBlue(RED_PIN, GREEN_PIN, BLUE_PIN):
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(BLUE_PIN, GPIO.HIGH)


def determine_color(buttonName):
    if buttonName == "1":
        return red
    elif buttonName == "2":
        return green
    elif buttonName == "3":
        return blue
    elif buttonName == "4":
        return yellow
    elif buttonName == "5":
        return white
    elif buttonName == "6":
        return purple
    elif buttonName == "7":
        return lightBlue
    else:
        return None


button_to_color_name = {
    "1": "red",
    "2": "green",
    "3": "blue",
    "4": "yellow",
    "5": "white",
    "6": "purple",
    "7": "lightBlue",
}

current_color_index = 0
colors = [red, green, blue, yellow, white, purple, lightBlue]
color_names = ["red", "green", "blue", "yellow", "white", "purple", "lightBlue"]


def change_color(direction, colors, color_names):
    global current_color_index
    if direction == "UP":
        current_color_index = (current_color_index + 1) % len(colors)
    elif direction == "DOWN":
        current_color_index = (current_color_index - 1) % len(colors)

    return color_names[current_color_index]


def rgb_loop(RED_PIN, GREEN_PIN, BLUE_PIN, stop_event, settings, publish_event, rgb_callback, print_lock, rgb_queue):
    global current_color_name

    try:
        setup(RED_PIN, GREEN_PIN, BLUE_PIN)
        while not stop_event.is_set():
            button = rgb_queue.get()

            if button == "UP" or button == "DOWN":
                current_color_name = change_color(button, colors, color_names)
                color_function = colors[current_color_index]
                color_function(RED_PIN, GREEN_PIN, BLUE_PIN)
                rgb_callback(settings, publish_event, current_color_name)  # Poziv callback-a sa imenom trenutne boje
            elif button in button_to_color_name:
                current_color_name = button_to_color_name[button]
                color_function = globals()[current_color_name]
                color_function(RED_PIN, GREEN_PIN, BLUE_PIN)
                rgb_callback(settings, publish_event, current_color_name)  # Poziv callback-a sa imenom trenutne boje
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nBRGB sensor stopped!")
    finally:
        GPIO.cleanup()
