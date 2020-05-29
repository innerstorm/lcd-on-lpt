#!/usr/bin/env python

import time ,datetime
import parallel
import atexit

from modules import *

def exit_handler():
    print('My application is ending!')
    lcd.clearScreen()


if __name__ == '__main__':

    lcd = LCD()

    atexit.register(exit_handler)

    while True:
        lcd.setCursorPos(1, 5)
        now = datetime.datetime.today().strftime('%H:%M:%S')
        lcd.write(now)
        time.sleep(.5)

