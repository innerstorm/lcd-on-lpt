#!/usr/bin/env python

import time ,datetime
import parallel

from modules import *

# convert an 8-bit number to a binary string
def convBinary(value):
    binaryValue = 'b'
    for  x in range(0,8):
        temp = value & 0x80
        if temp == 0x80:
            binaryValue = binaryValue + '1'
        else:
            binaryValue = binaryValue + '0'
        value = value << 1
    return binaryValue

# ------------------------------------------------------------------
def wait(sec):
    time.sleep(sec)
    return

# ----------------------------------------------------------------------------------------
if __name__ == '__main__':

    lcd = LCD()
    lcd.clearScreen()
    #lcd.setCursorOn()
    lcd.setCursorOff()
    #lcd.setCursorLine()

    lcd.setCursorPos(1,1)
    lcd.write('Csaba')
    wait(.5)
    
    #lcd.customChar()
    #lcd.customChar2()

    #wait(0)

    lcd.clearCharMemory()
    #lcd.defineCustomCharsWithPos(chars)

    lcd.loadCustomCharSet(GAUGES2)
    
    #lcd.setCursorPos(16,1)
    #lcd.writeCustomChar(1)
    #lcd.setCursorPos(1,2)
    #lcd.writeCustomChar(0)
    #lcd.defineCustomChars(sziv)
    #lcd.clearScreen()



#    while True:

    lcd.setCursorPos(1,1)
    for i in range(0,8):
        lcd.writeCustomChar(i)

    #now = datetime.datetime.today().strftime('%H-%M-%S')

    #now = int(round(time.time() * 1000))

    """
    start_time = time.time()

    i=1

    while True:
        elapsed = time.time() - start_time

        if elapsed % 0.5 == 0:
            print('0.5s')
            
        if elapsed % 1 == 0:
            print('1s')
            lcd.setCursorPos(16,2)
            lcd.write("A")
            lcd.setCursorPos(1,1)
            lcd.write(str(round(elapsed,2)))

        if elapsed % 2 == 0:
            print('2s')
            lcd.setCursorPos(1,2)
            lcd.write("B")

        if elapsed > 60:
            start_time = time.time()
    """

    """
    while True:
        lcd.setCursorPos(1,2)
        now = datetime.datetime.today().strftime('%H:%M:%S')
        lcd.write(now)
        wait(.1)
    """


    #lcd.clearScreen()


    print
    print "Done."
    exit