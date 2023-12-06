import random
import time


def simulated_gyro(print_lock, stop_event, settings, publish_event, gyro_callback):
    try:
        while True:
            if stop_event.is_set():
                break

            # Simulated Gyroscope Data (Raw and Converted)
            gyro_xyz_raw = [round(random.uniform(-32768, 32767), 2) for _ in range(3)]
            gyro_xyz_converted = [round(g / 131.0, 2) for g in gyro_xyz_raw]

            # Simulated Accelerometer Data (Raw and Converted)
            accel_xyz_raw = [round(random.uniform(-32768, 32767), 2) for _ in range(3)]
            accel_xyz_converted = [round(a / 16384.0, 2) for a in accel_xyz_raw]

            # Printing the simulated data
            with print_lock:
                print("a/g:%d\t%d\t%d\t%d\t%d\t%d " % tuple(accel_xyz_raw + gyro_xyz_raw))
                print("a/g:%.2f g\t%.2f g\t%.2f g\t%.2f d/s\t%.2f d/s\t%.2f d/s" % tuple(
                    accel_xyz_converted + gyro_xyz_converted))

            # Callbacks for further processing (if needed)

            gyro_value = str(gyro_xyz_converted)
            accel_value = str(accel_xyz_converted)
            gyro_callback(settings, publish_event, gyro_value, accel_value)

            time.sleep(3)

    except KeyboardInterrupt:
            print("\nSimulated Gyro sensor stopped!")

