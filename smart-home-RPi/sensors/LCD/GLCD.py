#!/usr/bin/env python3

from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD

from time import sleep, strftime
from datetime import datetime
import random


PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
class LCD(object):
    def __init__(self):
        try:
            self.mcp = PCF8574_GPIO(PCF8574_address)
        except:
            try:
                self.mcp = PCF8574_GPIO(PCF8574A_address)
            except:
                print('I2C Address Error !')
                exit(1)

        self.lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4, 5, 6, 7], GPIO=self.mcp)
        self.message = ""
    def display(self):
        self.mcp.output(3, 1)  # turn on LCD backlight
        self.lcd.begin(20, 2)  # set number of LCD lines and columns
        # lcd.clear()
        self.lcd.setCursor(0, 0)  # set cursor position
        self.lcd.message(self.message)


    def destroy(self):
        self.lcd.clear()


def run_lcd_loop(callback, stop_event, print_lock, settings, publish_event, queue):
    lcd = LCD()
    while True:
        h, t = queue.get()
        lcd.message = f"Temperature: {t} °C\nHumidity: {h}%"
        lcd.display()
        callback(lcd.message, print_lock, settings, settings, publish_event)

        if stop_event.is_set():
            lcd.destroy()
            break
        sleep(0.1)



