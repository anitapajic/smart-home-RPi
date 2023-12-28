
button_to_color_name = {
    "1": "red",
    "2": "green",
    "3": "blue",
    "4": "yellow",
    "5": "white",
    "6": "purple",
    "7": "lightBlue"
}
current_color_index = 0
color_names = ["red", "green", "blue", "yellow", "white", "purple", "lightBlue"]


def change_color(direction, color_names):
    global current_color_index
    if direction == "UP":
        current_color_index = (current_color_index + 1) % len(color_names)
    elif direction == "DOWN":
        current_color_index = (current_color_index - 1) % len(color_names)

    return color_names[current_color_index]


def simulated_rgb(rgb_name, print_lock, stop_event, settings, publish_event, rgb_callback, rgb_queue):
    while True:
        if stop_event.is_set():
            break
        taster = rgb_queue.get()
        if taster == "UP" or taster == "DOWN":
            current_color_name = change_color(taster, color_names)
            rgb_callback(settings, publish_event,
                         current_color_name)
            with print_lock:
                print("UPALJENO SVETLO : ", current_color_name)
        elif taster in button_to_color_name:
            current_color_name = button_to_color_name[taster]
            rgb_callback(settings, publish_event, current_color_name)
            with print_lock:
                print("UPALJENO SVETLO : ", current_color_name)
        else:
            with print_lock:
                print("No color is shown on ", rgb_name)
