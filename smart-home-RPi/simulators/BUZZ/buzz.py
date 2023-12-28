import time
# def simulated_buzz(pitch, duration, settings, publish_event, buzz_callback):
#     try:
#         import subprocess
#         volume = 1.0
#         rate = 0.5
#         audio_file = '/System/Library/Sounds/Funk.aiff'
#         subprocess.run(['afplay', '-v', str(volume), '-r', str(rate), audio_file])
#         buzz_callback(settings, publish_event, 1)
#     except subprocess.CalledProcessError as e:
#         print(f"Error playing audio: {e}")
#         time.sleep(10)
#
#     except Exception as e:
#         print(f"Unexpected error: {e}")
#         time.sleep(10)

def simulated_buzz(pitch, duration, settings, publish_event, buzz_callback):
    try:
        import winsound
        winsound.Beep(pitch, duration)
        buzz_callback(settings, publish_event, 1)
    except ImportError:
        print("winsound module is not available on this system.")
        time.sleep(1)

def listen_for_keypress(stop_event, print_lock, pitch, duration, settings, publish_event, buzz_callback, alarm):
    while not stop_event.is_set():
        alarm.wait()
        simulated_buzz(pitch, duration, settings, publish_event, buzz_callback)
        # alarm.clear()
