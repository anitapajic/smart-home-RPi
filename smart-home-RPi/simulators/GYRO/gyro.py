import random
import time


def generate_sensor_data():
    """Generiše simulirane podatke za žiroskop i akcelerometar."""
    gyro_data = [round(random.uniform(-32768, 32767), 2) for _ in range(3)]
    accel_data = [round(random.uniform(-32768, 32767), 2) for _ in range(3)]
    return gyro_data, accel_data


def convert_sensor_data(raw_data, conversion_factor):
    """Konvertuje sirove podatke senzora u fizičke jedinice."""
    return [round(d / conversion_factor, 2) for d in raw_data]


def detect_unusual_activity(gyro_data, accel_data, gyro_threshold=250.0, accel_threshold=3.9):
    if any(abs(g) > gyro_threshold for g in gyro_data):
        return True
    if any(abs(a - 1) > accel_threshold for a in accel_data):  # Oduzimamo 1 da uklonimo uticaj gravitacije
        return True
    return False


def simulated_gyro(print_lock, stop_event, settings, publish_event, gyro_callback, alarm_event, alarm_reason_queue):
    try:
        gyro_threshold = 250.0  # Prag za žiroskop
        accel_threshold = 1.9  # Prag za akcelerometar
        while True:
            if stop_event.is_set():
                break
            gyro_raw, accel_raw = generate_sensor_data()
            gyro_converted = convert_sensor_data(gyro_raw, 131.0)
            accel_converted = convert_sensor_data(accel_raw, 16384.0)
            gyro_value = str(gyro_converted)
            accel_value = str(accel_converted)

            gyro_callback(settings, publish_event, gyro_value, accel_value)

            if detect_unusual_activity(gyro_converted, accel_converted, gyro_threshold, accel_threshold):
                with print_lock:
                    print("Neobična aktivnost detektovana! Aktiviranje alarma.")
                alarm_event.set()
                alarm_reason_queue.put("Gyroscope detected unusual activity.")

            time.sleep(7)

    except KeyboardInterrupt:
            print("\nSimulated Gyro sensor stopped!")

