#!/usr/bin/python

"""
menu with message view and physical steering
"""

from rpilcdmenu import *
from rpilcdmenu.items import *

import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from RPi import GPIO
import adafruit_bitbangio as bitbangio
import time


def main():
    # create menu as in example3
    menu = RpiLCDMenu(7, 8, [25, 24, 23, 15])

    menu.append_item(
        MessageItem('message item',
                    'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut '
                    'labore et dolore magna aliqua.',
                    menu,
                    True)
    )

    menu.start()

    # setup the rotary encoder pins
    rot_clk = 17
    rot_dt = 27
    # set GPIO pins
    GPIO.setmode(GPIO.BCM)
    # set to GPIO.PUD_UP as the TEAC panel uses an encoder that is grounded
    GPIO.setup(rot_clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(rot_dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # set default counter variable
    counter = 0
    clkLastState = GPIO.input(rot_clk)

    # mcp3008 button reader setup
    # create software spi
    spi = bitbangio.SPI(board.D11, MISO=board.D9, MOSI=board.D10)
    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D22)
    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)
    # create analog input channels on pins 6 and 7 of the mcp3008
    chan1 = AnalogIn(mcp, MCP.P6)
    chan2 = AnalogIn(mcp, MCP.P7)

    # main loop
    while True:
        # read button states
        if 0 <= chan1.value <= 1000:
            print("Timer button pressed" + str(chan1.value))
            time.sleep(0.5)
        if 5900 <= chan1.value <= 7000:
            print("Time Adj button pressed" + str(chan1.value))
            time.sleep(0.5)
        if 12000 <= chan1.value <= 13000:
            print("Daily button pressed" + str(chan1.value))
            time.sleep(0.5)
        if 0 <= chan2.value <= 1000:
            print("Power button pressed" + str(chan2.value))
            time.sleep(0.5)
        if 5800 <= chan2.value <= 6100:
            print("Band button pressed " + str(chan2.value))
            time.sleep(0.5)
        if 13000 <= chan2.value <= 14000:
            print("Function button pressed" + str(chan2.value))
            time.sleep(0.5)
        if 26000 <= chan2.value <= 27000:
            print("Enter button pressed" + str(chan2.value))
            menu = menu.processEnter()
            time.sleep(0.5)
        if 19000 <= chan2.value <= 21000:
            print("Info button pressed" + str(chan2.value))
            time.sleep(0.5)
        if 39000 <= chan2.value <= 41000:
            print("Auto Tuning button pressed" + str(chan2.value))
            time.sleep(0.5)
        if 33000 <= chan2.value <= 34000:
            print("Memory button pressed" + str(chan2.value))
            time.sleep(0.5)
        if 44000 <= chan2.value <= 46000:
            print("Dimmer button pressed" + str(chan2.value))
            time.sleep(0.5)
        # buttons depressed

        # read rotary encoder states
        clkState = GPIO.input(rot_clk)
        dtState = GPIO.input(rot_dt)
        if clkState != clkLastState:
            if dtState != clkState:
                counter += 1
                menu = menu.processUp()
            else:
                counter -= 1
                menu = menu.processDown()
            print(counter)
        clkLastState = clkState

def exit_sub_menu(submenu):
    return submenu.exit()


if __name__ == "__main__":
    main()