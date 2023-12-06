import sys
import threading
from settings import load_settings
from components.LED_DIODE.led_diode import run_dl
import time
from threading import Lock
from components.BUZZ.buzz import run_db1, run_bb


print_lock = Lock()

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass


def print_menu():
    print("----------------------------------------------")
    print("Select which sensor you want to simulate:")
    print("1. DB1")
    print("2. DL1")
    print("3. BB")
    print("Enter Q to exit the application..")
    print("----------------------------------------------")
    choice = input("Enter your choice: ").strip()
    return choice


def handle_choice(choice):
    if choice.lower() == 'q':
        sys.exit(0)

    enter_thread = threading.Thread(target=listen_for_stop_command, args=(stop_event,))
    enter_thread.start()
    if choice == '1':
        db1_settings = settings['DB1']
        run_db1(db1_settings, threads, stop_event, print_lock)
    elif choice == '2':
        dl_settings = settings['DL']
        run_dl(dl_settings, threads, stop_event, print_lock)
    elif choice == '3':
        bb_settings = settings['BB']
        run_bb(bb_settings, threads, stop_event, print_lock)
    else:
        print("Invalid choice. Please try again.")

    for thread in threads:
        thread.join()


def listen_for_stop_command(stop_event):
    command = input("Press '0' to stop all simulations and return to the menu...\n")
    if command == '0':
        stop_event.set()


if __name__ == "__main__":
    print('Starting app')
    settings = load_settings()
    threads = []
    stop_event = threading.Event()
    try:
        while True:
            choice = print_menu()  # Get the user's choice
            handle_choice(choice)  # Handle the choice and wait for simulations to end
            stop_event.clear()
            threads = []

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()
