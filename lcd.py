import subprocess
import psutil
import time ,datetime
import schedule
import parallel
import atexit

from modules import *


def sleep(sec):
    time.sleep(sec)


def disk_free():
    mount_point = "/media/server/raid"
    df = psutil.disk_usage(mount_point).free
    df = round(df/1024.0**4, 2)
    lcd.setCursorPos(0,0)
    lcd.write(str(df))


def cpu_usage():
    percent = psutil.cpu_percent()
    usage = percent
    lcd.setCursorPos(1,1)
    lcd.write(str(usage))


def cpu_temp():
    temperatures = psutil.sensors_temperatures()
    temp = temperatures['coretemp'][0][1]
    lcd.setCursorPos(1,7)
    lcd.write(str(temp))


def free_love():
    lcd.setCursorPos(0,0)
    lcd.write('456')


def clock():
    lcd.setCursorPos(1, 12)
    now = datetime.datetime.today().strftime('%H:%M')
    lcd.write(now)


if __name__ == '__main__':
    
    lcd = LCD()
    
    clock()
    disk_free()
    cpu_usage()
    cpu_temp()
    
    schedule.every(10).seconds.do(clock)
    schedule.every(10).minutes.do(disk_free)
    schedule.every(10).seconds.do(cpu_usage)
    schedule.every(10).seconds.do(cpu_temp)

    while True:
        schedule.run_pending()
        sleep(1)