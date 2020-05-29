#!/usr/bin/env python
import time
import datetime
import parallel

# variables
TIME_PULSE = 0.005

CHAR_HEART   = [0b00000, 0b01010, 0b11111, 0b11111, 0b01110, 0b00100, 0b00000, 0b00000]
CHAR_BELL    = [0b00100, 0b01110, 0b01110, 0b01110, 0b01110, 0b11111, 0b00100, 0b00000]
CHAR_BATTERY = [0b01110, 0b11011, 0b10001, 0b10001, 0b10001, 0b11111, 0b11011, 0b00000]

CHARS = [
    CHAR_HEART, 
    CHAR_BELL,
    CHAR_BATTERY
]

GAUGES = [
    [0b10000,0b10000,0b10000,0b10000,0b10000,0b10000,0b10000,0b10000],
    [0b11000,0b11000,0b11000,0b11000,0b11000,0b11000,0b11000,0b11000],
    [0b11100,0b11100,0b11100,0b11100,0b11100,0b11100,0b11100,0b11100],
    [0b11110,0b11110,0b11110,0b11110,0b11110,0b11110,0b11110,0b11110],
    [0b11111,0b11111,0b11111,0b11111,0b11111,0b11111,0b11111,0b11111]
]

GAUGES2 = [
    [0b00000,0b00000,0b00000,0b00000,0b00000,0b00000,0b00000,0b11111],
    [0b00000,0b00000,0b00000,0b00000,0b00000,0b00000,0b11111,0b11111],
    [0b00000,0b00000,0b00000,0b00000,0b00000,0b11111,0b11111,0b11111],
    [0b00000,0b00000,0b00000,0b00000,0b11111,0b11111,0b11111,0b11111],
    [0b00000,0b00000,0b00000,0b11111,0b11111,0b11111,0b11111,0b11111],
    [0b00000,0b00000,0b11111,0b11111,0b11111,0b11111,0b11111,0b11111],
    [0b00000,0b11111,0b11111,0b11111,0b11111,0b11111,0b11111,0b11111],
    [0b11111,0b11111,0b11111,0b11111,0b11111,0b11111,0b11111,0b11111],
]


# command codes

LCDON = 0x01  #0x0000-0001 Switch on  display
LCDOFF = 0x08  #0x0000-1000 Switch off display
LCDCLEAR = 0x01  #0x0000-0001

LCDLINE1 = 0x80  #0x1000-0000
LCDLINE2 = 0xc0  #0x1100-0000

LCDCURSORON = 0x0f  #0x0000-1111 turn on cursor blinking
LCDCURSOROFF = 0x0c  #0x0000-1100 Disable cursor blinking. The cursor is hidden.
LCDCURSORHOME = 0x02  # Home (move cursor to top/left character position)

LCDCURSORBLINKING = 0x0f
LCDCURSORSTEADY = 0x0e

LCDCGADRSET = 0x40  #0b0100-0000
LCDDDADRSET = 0x80  #0b1000-0000
LCD2LINES = 0x38  #0b0010-1000 Set display mode to two lines.

LCD8BITS = 0x30  #0b0011-0000 select 8 Bit interface
LCD4BITS = 0x20  #0b0010-0000 select 4 Bit interface
LCD_DATA_OFF = 0x05  #0x0000-0101 mask used to clear the data lines

"""
Scroll display one character right (all lines): 0x1E
Scroll display one character left (all lines): 0x18

Move cursor one character left: 0x10
Move cursor one character right: 0x14

Blank the display (without clearing): 0x08
Restore the display (with cursor hidden): 0x0C

#command(0x04) # move cursor right, dont shift display
#command(0x05) # move cursor right, do shift display (left)
#command(0x06) # move cursor right, dont shift display (this is the most common)
#command(0x07) # move cursor right, do shift display (left)
"""

# --------------------------------------------------------------------
class LCD(object):


    def __init__(self):
        self.p = parallel.Parallel()

        self.char_mem_pos = LCDCGADRSET
        self.data = 0
        self.p.setDataStrobe(0)
        self.p.setAutoFeed(0)
        self.p.setInitOut(1)
        
        self.setRS(0)
        self.setRW(0)
        self.out(0)  #reset pins

        """    
        time.sleep(0.050)           #wait more than 30ms
        self.out(LCD8BITS)          #set 8 bit interface

        self.pulseE()              #toggle LCD_E, the enable pin
        time.sleep(0.005)           #wait a bit
        self.pulseE()              #toggle LCD_E, the enable pin
        time.sleep(0.005)           #wait a bit
        self.pulseE()              #toggle LCD_E, the enable pin
        time.sleep(0.005)           #wait a bit
        """

        # set 8bits comm
        self.instr(LCD8BITS)

        # setup 16x2 LCD
        self.instr(LCD2LINES)

        # display ON
        self.instr(LCDCLEAR)

        #hide cursor
        self.instr(LCDCURSOROFF)



    # not used when only writing to lcd
    # pin is grounded
    def setRW(self, state):
        self.p.setAutoFeed(state)

    # 0 - command
    # 1 - data
    def setRS(self, state):
        self.p.setSelect(state)

    # set E to true to apply command
    def pulseE(self):
        self.p.setInitOut(0)
        time.sleep(TIME_PULSE)
        self.p.setInitOut(1)

    # setData wrapper
    def out(self, data):
        self.data = data
        self.p.setData(self.data)

    # send instruction byte to LCD
    def instr(self, cmd):
        self.out(cmd)
        self.setRS(0)
        #self.setRW(0)
        self.pulseE()  #toggle LCD_E, the enable pin
        time.sleep(TIME_PULSE)  #wait until instr is finished

    # cursor settings
    def setCursorOn(self):
        self.instr(LCDCURSORON)

    def setCursorOff(self):
        self.instr(LCDCURSOROFF)

    def setCursorBlock(self):
        self.instr(LCDCURSORBLINKING)

    def setCursorLine(self):
        self.instr(LCDCURSORSTEADY)

    def setCursorPos(self, col, row):
        # 1. row: 0x80 + hex([0..15])
        # 2. row: 0xC0 + hex([0..15])
        coords = 128
        if col == 2: coords = 192
        row -= 1
        coords += row
        self.instr(coords)

    # screen commands
    def clearScreen(self):
        self.instr(LCDCLEAR)
        self.instr(LCDCURSORHOME)


    # send a data byte to the LCD
    # write character
    def putc(self, c):
        self.out(ord(c))
        self.setRS(1)
        #self.setRW(0)
        self.pulseE()
        time.sleep(TIME_PULSE)
    
    # write string
    def write(self, str):
        l = len(str)
        self.setRS(1)
        for i in range(0, l):
            #print(ord(str[i]))
            self.out(ord(str[i]))
            self.pulseE()
        self.setRS(0)


        













    # write char code   
    def printCode(self, c):
        self.setRS(1)
        self.out(c)
        self.pulseE()
        self.setRS(0)


    def customChar(self):
        self.instr(0x40)
        self.setRS(1)

        for i in range(0,8):
            self.out(CHAR_BELL[i])
            print(CHAR_BELL[i])
            self.pulseE()

        #self.setCursorPos(0,0)

        self.setRS(1)
        self.out(0x00)
        self.pulseE()

    # --------------------
    def customChar2(self):
        # address of CGRAM
        self.instr(0x48)
        
        # set Data flow
        self.setRS(1)

        # create char at the given address
        for i in range(0,8):
            self.out(CHAR_BATTERY[i])
            print(CHAR_BATTERY[i])
            self.pulseE()

        # write
        self.setCursorPos(0,0)
        self.setRS(1)
        self.out(0x01)
        self.pulseE()


    # ---------------------------------
    def loadCustomCharSet(self, CHARS):
        # pointing to 0x40 by default
        self.instr(self.char_mem_pos)
        
        # if we have max eight chars
        if len(CHARS) in range(1,9):
        
            # iterate the cahrset
            for k in range(0, len(CHARS)):
                #set data flag
                self.setRS(1)
                
                # write rows of char in the memory
                for i in range(0, 8):
                    self.out(CHARS[k][i])
                    self.pulseE()

        # reset data flag, 'cause why not?
        self.setRS(0)


    # wipe out the character memory
    def clearCharMemory(self):
        self.instr(LCDCGADRSET)
        for i in range(0,9):
            self.setRS(1)
            for i in range(0, 8):
                self.out(0b00000)
                self.pulseE()



    def writeCustomChar(self, idx):
        self.setRS(1)
        self.out(idx)
        self.pulseE()
