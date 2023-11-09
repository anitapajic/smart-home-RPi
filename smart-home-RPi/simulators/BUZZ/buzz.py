import threading
import time
import keyboard

# Simulated buzzer function with winsound
def simulated_buzz(pitch, duration):
    try:
        import winsound
        # Use the pitch and duration passed to the function
        winsound.Beep(pitch, duration)
    except ImportError:
        print("winsound module is not available on this system.")

def listen_for_keypress(stop_event, print_lock, key='x'):
    print(f"Press '{key}' to activate the simulated buzzer.")
    while not stop_event.is_set():
        try:
            if keyboard.is_pressed(key):  # Make sure 'key' is a string like 'x'
                with print_lock:
                    print("Buzzer activated!")
                simulated_buzz(440, 1000)  # You may adjust pitch and duration
                time.sleep(1)  # Prevent continuous triggering
        except Exception as e:
            with print_lock:
                print(f"An error occurred: {e}")
                break