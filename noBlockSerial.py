#Non Blocking Serial Code for Python

import serial
import time

ser = serial.Serial('COM5', baudrate = 115200)

print("""\
                    __  _____           _       __
   __  _____  ___  / /_/ ___/___  _____(_)___ _/ /
  / / / / _ \/ _ \/ __/\__ \/ _ \/ ___/ / __ `/ / 
 / /_/ /  __/  __/ /_ ___/ /  __/ /  / / /_/ / /  
 \__, /\___/\___/\__//____/\___/_/  /_/\__,_/_/   
/____/                                            
    """)

print("Send command to listed Serial:")

while (True):
    if (ser.in_waiting):
        buf = ser.read(ser.in_waiting)
        print(buf)
        time.sleep(0.01)
