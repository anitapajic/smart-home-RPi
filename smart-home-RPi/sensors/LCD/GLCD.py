# #!/usr/bin/env python3
#
import smbus
import time
from time import sleep

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


class PCF8574_I2C(object):
    OUPUT = 0
    INPUT = 1

    def __init__(self, address):
        # Note you need to change the bus number to 0 if running on a revision 1 Raspberry Pi.
        self.bus = smbus.SMBus(1)
        self.address = address
        self.currentValue = 0
        self.writeByte(0)  # I2C test.

    def readByte(self):  # Read PCF8574 all port of the data
        # value = self.bus.read_byte(self.address)
        return self.currentValue  # value

    def writeByte(self, value):  # Write data to PCF8574 port
        self.currentValue = value
        self.bus.write_byte(self.address, value)

    def digitalRead(self, pin):  # Read PCF8574 one port of the data
        value = self.readByte()
        return (value & (1 << pin) == (1 << pin)) and 1 or 0

    def digitalWrite(self, pin, newvalue):  # Write data to PCF8574 one port
        value = self.currentValue  # bus.read_byte(address)
        if (newvalue == 1):
            value |= (1 << pin)
        elif (newvalue == 0):
            value &= ~(1 << pin)
        self.writeByte(value)


def loop():
    mcp = PCF8574_I2C(0x27)
    while True:
        # mcp.writeByte(0xff)
        mcp.digitalWrite(3, 1)
        print('Is 0xff? %x' % (mcp.readByte()))
        time.sleep(1)
        mcp.writeByte(0x00)
        # mcp.digitalWrite(7,1)
        print('Is 0x00? %x' % (mcp.readByte()))
        time.sleep(1)


class PCF8574_GPIO(object):  # Standardization function interface
    OUT = 0
    IN = 1
    BCM = 0
    BOARD = 0

    def __init__(self, address):
        self.chip = PCF8574_I2C(address)
        self.address = address

    def setmode(self, mode):  # PCF8574 port belongs to two-way IO, do not need to set the input and output model
        pass

    def setup(self, pin, mode):
        pass

    def input(self, pin):  # Read PCF8574 one port of the data
        return self.chip.digitalRead(pin)

    def output(self, pin, value):  # Write data to PCF8574 one port
        self.chip.digitalWrite(pin, value)


def destroy():
    bus.close()


# if __name__ == '__main__':
# 	print ('Program is starting ... ')
# 	try:
# 		loop()
# 	except KeyboardInterrupt:
# 		destroy()


class Adafruit_CharLCD(object):

    # commands
    LCD_CLEARDISPLAY        = 0x01
    LCD_RETURNHOME          = 0x02
    LCD_ENTRYMODESET        = 0x04
    LCD_DISPLAYCONTROL      = 0x08
    LCD_CURSORSHIFT         = 0x10
    LCD_FUNCTIONSET         = 0x20
    LCD_SETCGRAMADDR        = 0x40
    LCD_SETDDRAMADDR        = 0x80

    # flags for display entry mode
    LCD_ENTRYRIGHT          = 0x00
    LCD_ENTRYLEFT           = 0x02
    LCD_ENTRYSHIFTINCREMENT = 0x01
    LCD_ENTRYSHIFTDECREMENT = 0x00

    # flags for display on/off control
    LCD_DISPLAYON           = 0x04
    LCD_DISPLAYOFF          = 0x00
    LCD_CURSORON            = 0x02
    LCD_CURSOROFF           = 0x00
    LCD_BLINKON             = 0x01
    LCD_BLINKOFF            = 0x00

    # flags for display/cursor shift
    LCD_DISPLAYMOVE         = 0x08
    LCD_CURSORMOVE          = 0x00

    # flags for display/cursor shift
    LCD_DISPLAYMOVE         = 0x08
    LCD_CURSORMOVE          = 0x00
    LCD_MOVERIGHT           = 0x04
    LCD_MOVELEFT            = 0x00

    # flags for function set
    LCD_8BITMODE            = 0x10
    LCD_4BITMODE            = 0x00
    LCD_2LINE               = 0x08
    LCD_1LINE               = 0x00
    LCD_5x10DOTS            = 0x04
    LCD_5x8DOTS             = 0x00

    def __init__(self, pin_rs=25, pin_e=24, pins_db=[23, 17, 21, 22], GPIO=None):
        # Emulate the old behavior of using RPi.GPIO if we haven't been given
        # an explicit GPIO interface to use
        if not GPIO:
            import RPi.GPIO as GPIO
            GPIO.setwarnings(False)
        self.GPIO = GPIO
        self.pin_rs = pin_rs
        self.pin_e = pin_e
        self.pins_db = pins_db

        self.GPIO.setmode(GPIO.BCM) #GPIO=None use Raspi PIN in BCM mode
        self.GPIO.setup(self.pin_e, GPIO.OUT)
        self.GPIO.setup(self.pin_rs, GPIO.OUT)

        for pin in self.pins_db:
            self.GPIO.setup(pin, GPIO.OUT)

        self.write4bits(0x33)  # initialization
        self.write4bits(0x32)  # initialization
        self.write4bits(0x28)  # 2 line 5x7 matrix
        self.write4bits(0x0C)  # turn cursor off 0x0E to enable cursor
        self.write4bits(0x06)  # shift cursor right

        self.displaycontrol = self.LCD_DISPLAYON | self.LCD_CURSOROFF | self.LCD_BLINKOFF

        self.displayfunction = self.LCD_4BITMODE | self.LCD_1LINE | self.LCD_5x8DOTS
        self.displayfunction |= self.LCD_2LINE

        # Initialize to default text direction (for romance languages)
        self.displaymode = self.LCD_ENTRYLEFT | self.LCD_ENTRYSHIFTDECREMENT
        self.write4bits(self.LCD_ENTRYMODESET | self.displaymode)  # set the entry mode

        self.clear()

    def begin(self, cols, lines):
        if (lines > 1):
            self.numlines = lines
            self.displayfunction |= self.LCD_2LINE

    def home(self):
        self.write4bits(self.LCD_RETURNHOME)  # set cursor position to zero
        self.delayMicroseconds(3000)  # this command takes a long time!

    def clear(self):
        self.write4bits(self.LCD_CLEARDISPLAY)  # command to clear display
        self.delayMicroseconds(3000)  # 3000 microsecond sleep, clearing the display takes a long time

    def setCursor(self, col, row):
        self.row_offsets = [0x00, 0x40, 0x14, 0x54]
        if row > self.numlines:
            row = self.numlines - 1  # we count rows starting w/0
        self.write4bits(self.LCD_SETDDRAMADDR | (col + self.row_offsets[row]))

    def noDisplay(self):
        """ Turn the display off (quickly) """
        self.displaycontrol &= ~self.LCD_DISPLAYON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def display(self):
        """ Turn the display on (quickly) """
        self.displaycontrol |= self.LCD_DISPLAYON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def noCursor(self):
        """ Turns the underline cursor off """
        self.displaycontrol &= ~self.LCD_CURSORON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def cursor(self):
        """ Turns the underline cursor on """
        self.displaycontrol |= self.LCD_CURSORON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def noBlink(self):
        """ Turn the blinking cursor off """
        self.displaycontrol &= ~self.LCD_BLINKON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def blink(self):
        """ Turn the blinking cursor on """
        self.displaycontrol |= self.LCD_BLINKON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def DisplayLeft(self):
        """ These commands scroll the display without changing the RAM """
        self.write4bits(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVELEFT)

    def scrollDisplayRight(self):
        """ These commands scroll the display without changing the RAM """
        self.write4bits(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVERIGHT)

    def leftToRight(self):
        """ This is for text that flows Left to Right """
        self.displaymode |= self.LCD_ENTRYLEFT
        self.write4bits(self.LCD_ENTRYMODESET | self.displaymode)

    def rightToLeft(self):
        """ This is for text that flows Right to Left """
        self.displaymode &= ~self.LCD_ENTRYLEFT
        self.write4bits(self.LCD_ENTRYMODESET | self.displaymode)

    def autoscroll(self):
        """ This will 'right justify' text from the cursor """
        self.displaymode |= self.LCD_ENTRYSHIFTINCREMENT
        self.write4bits(self.LCD_ENTRYMODESET | self.displaymode)

    def noAutoscroll(self):
        """ This will 'left justify' text from the cursor """
        self.displaymode &= ~self.LCD_ENTRYSHIFTINCREMENT
        self.write4bits(self.LCD_ENTRYMODESET | self.displaymode)

    def write4bits(self, bits, char_mode=False):
        """ Send command to LCD """
        self.delayMicroseconds(1000)  # 1000 microsecond sleep
        bits = bin(bits)[2:].zfill(8)
        self.GPIO.output(self.pin_rs, char_mode)
        for pin in self.pins_db:
            self.GPIO.output(pin, False)
        for i in range(4):
            if bits[i] == "1":
                self.GPIO.output(self.pins_db[::-1][i], True)
        self.pulseEnable()
        for pin in self.pins_db:
            self.GPIO.output(pin, False)
        for i in range(4, 8):
            if bits[i] == "1":
                self.GPIO.output(self.pins_db[::-1][i-4], True)
        self.pulseEnable()

    def delayMicroseconds(self, microseconds):
        seconds = microseconds / float(1000000)  # divide microseconds by 1 million for seconds
        sleep(seconds)

    def pulseEnable(self):
        self.GPIO.output(self.pin_e, False)
        self.delayMicroseconds(1)       # 1 microsecond pause - enable pulse must be > 450ns
        self.GPIO.output(self.pin_e, True)
        self.delayMicroseconds(1)       # 1 microsecond pause - enable pulse must be > 450ns
        self.GPIO.output(self.pin_e, False)
        self.delayMicroseconds(1)       # commands need > 37us to settle

    def message(self, text):
        """ Send string to LCD. Newline wraps to second line"""
        for char in text:
            if char == '\n':
                self.write4bits(0xC0)  # next line
            else:
                self.write4bits(ord(char), True)

#
# if __name__ == '__main__':
#     lcd = Adafruit_CharLCD()
#     lcd.clear()
#     lcd.message("  Adafruit 16x2\n  Standard LCD")

# !/usr/bin/env python3
#
#
# from time import sleep, strftime
# from datetime import datetime
#
#
# def get_cpu_temp():  # get CPU temperature and store it into file "/sys/class/thermal/thermal_zone0/temp"
#     tmp = open('/sys/class/thermal/thermal_zone0/temp')
#     cpu = tmp.read()
#     tmp.close()
#     return '{:.2f}'.format(float(cpu) / 1000) + ' C'
#
#
# def get_time_now():  # get system time
#     return datetime.now().strftime('    %H:%M:%S')
#
#
# def loop():
#     mcp.output(3, 1)  # turn on LCD backlight
#     lcd.begin(16, 2)  # set number of LCD lines and columns
#     while (True):
#         # lcd.clear()
#         lcd.setCursor(0, 0)  # set cursor position
#         lcd.message('CPU: ' + get_cpu_temp() + '\n')  # display CPU temperature
#         lcd.message(get_time_now())  # display the time
#         sleep(1)
#
#
# def destroy():
#     lcd.clear()
#
#
# PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
# PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
# # Create PCF8574 GPIO adapter.
# try:
#     mcp = PCF8574_GPIO(PCF8574_address)
# except:
#     try:
#         mcp = PCF8574_GPIO(PCF8574A_address)
#     except:
#         print('I2C Address Error !')
#         exit(1)
# # Create LCD, passing in MCP GPIO adapter.
# lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4, 5, 6, 7], GPIO=mcp)
#



