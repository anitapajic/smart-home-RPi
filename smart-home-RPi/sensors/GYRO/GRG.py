#!/usr/bin/env python3
import MPU6050
import time
import os

mpu = MPU6050.MPU6050()  # instantiate a MPU6050 class object
accel = [0] * 3  # store accelerometer data
gyro = [0] * 3  # store gyroscope data


def setup():
    mpu.dmp_initialize()  # initialize MPU6050


def loop(settings, publish_event, gyro_callback, stop_event, print_lock, alarm_event):
    while True:
        if stop_event.is_set():
            break
        accel = mpu.get_acceleration()  # get accelerometer data
        gyro = mpu.get_rotation()  # get gyroscope data

        # Convert raw data to lists
        accel_xyz_raw = [accel[0], accel[1], accel[2]]
        gyro_xyz_raw = [gyro[0], gyro[1], gyro[2]]

        # Convert raw data to physical units
        accel_xyz_converted = [round(a / 16384.0, 2) for a in accel_xyz_raw]
        gyro_xyz_converted = [round(g / 131.0, 2) for g in gyro_xyz_raw]

        os.system('clear')
        print("a/g:%d\t%d\t%d\t%d\t%d\t%d " % (accel[0], accel[1], accel[2], gyro[0], gyro[1], gyro[2]))
        print("a/g:%.2f g\t%.2f g\t%.2f g\t%.2f d/s\t%.2f d/s\t%.2f d/s" % (accel[0] / 16384.0, accel[1] / 16384.0,
                                                                            accel[2] / 16384.0, gyro[0] / 131.0,
                                                                            gyro[1] / 131.0, gyro[2] / 131.0))
        gyro_value = str(gyro_xyz_converted)
        accel_value = str(accel_xyz_converted)
        gyro_callback(settings, publish_event, gyro_value, accel_value)

        with print_lock:
            print("Ziroskop: ", gyro_value)
            print("Accelometar: ", accel_value)

        if detect_unusual_activity(gyro_xyz_converted, accel_xyz_converted):
            with print_lock:
                print("Neobična aktivnost detektovana! Aktiviranje alarma.")
            alarm_event.set()

        time.sleep(3)


def detect_unusual_activity(gyro_data, accel_data, gyro_threshold=250.0, accel_threshold=3.9):
    # Detekcija značajnih rotacija
    if any(abs(g) > gyro_threshold for g in gyro_data):
        return True

    # Detekcija značajnih pokreta ili udaraca
    if any(abs(a - 1) > accel_threshold for a in accel_data):  # Oduzimamo 1 da uklonimo uticaj gravitacije
        return True

    return False


def run_gyro_loop(print_lock, stop_event, settings, publish_event, gyro_callback, alarm_event):  # Program start from here
    print("Program is starting ... ")
    setup()
    try:
        loop(settings, publish_event, gyro_callback, stop_event, print_lock, alarm_event)
    except KeyboardInterrupt:
        pass
