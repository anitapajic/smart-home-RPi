#!/usr/bin/env python3
import MPU6050
import time
import os

mpu = MPU6050.MPU6050()  # instantiate a MPU6050 class object
accel = [0] * 3  # store accelerometer data
gyro = [0] * 3  # store gyroscope data


def setup():
    mpu.dmp_initialize()  # initialize MPU6050


def loop(settings, publish_event, gyro_callback):
    while True:
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
        time.sleep(1)


def run_gyro_loop(settings, publish_event, gyro_callback):  # Program start from here
    print("Program is starting ... ")
    setup()
    try:
        loop(settings, publish_event, gyro_callback)
    except KeyboardInterrupt:
        pass
