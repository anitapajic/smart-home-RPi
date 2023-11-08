
import threading
from settings import load_settings
from components.DHT.dht import run_dht1, run_dht2
from components.LED_DIODE.led_diode import run_dl
import time
from threading import Lock
from components.BUZZ.buzz import run_db1
from simulators.BUZZ.buzz import listen_for_keypress, simulated_buzz

print_lock = Lock()


try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass

def print_menu():
    print("----------------------------------------------")
    print("Select which sensor you want to simulate:")
    print("1. RDHT1 and RDHT2")
    print("2. DB1")
    print("3. RPIR1 and RPIR2")
    print("4. DPIR")
    print("5. DS1")
    print("6. DL1")
    print("7. DUDS1")
    print("8. DMS1")
    print("----------------------------------------------")

def handle_choice(choice):
    if choice == '1':
        dht1_settings = settings['DHT1']
        run_dht1(dht1_settings, threads, stop_event, print_lock)
        dht2_settings = settings['DHT2']
        run_dht2(dht2_settings, threads, stop_event, print_lock)

    elif choice == '2':
        db1_settings = settings['DB1']
        run_db1(db1_settings, threads, stop_event, print_lock)
        key_listener_thread = threading.Thread(target=listen_for_keypress, args=(stop_event, print_lock, 'x'))
        key_listener_thread.start()
        threads.append(key_listener_thread)

    elif choice == '3':
        dl_settings = settings['DL']
        run_dl(dl_settings, threads, stop_event, print_lock)
    elif choice == '4':
        print("Not yet implemented..")
    elif choice == '5':
        print("Not yet implemented..")
    elif choice == '6':
        print("Not yet implemented..")
    elif choice == '7':
        print("Not yet implemented..")
    elif choice == '8':
        print("Not yet implemented..")
    else:
        print("Invalid choice. Please try again.")


if __name__ == "__main__":
    print('Starting app')
    settings = load_settings()
    threads = []
    stop_event = threading.Event()
    try:
        while True:
            print_menu()
            choice = input("Enter your choice: ")
            if handle_choice(choice):
                break
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()
