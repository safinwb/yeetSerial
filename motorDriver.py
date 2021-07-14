#!/usr/bin/env python
import rospy
import time
from geometry_msgs.msg import Twist
import serial
import libscrc

l_speed = 0
r_speed = 0

ser = serial.Serial('/dev/motorDriver', baudrate = 115200)
print(ser.name + " is open")


def serialRx():
    if (ser.in_waiting):
        buf = ser.read(ser.in_waiting)
        print(buf)


def cmd_vel_cb(data):
    #rospy.loginfo("Linear: %s , Thetha: %s", data.linear.x, data.angular.z)
    global l_speed
    global r_speed

    demand_x = data.linear.x
    demand_z = data.angular.z

    l_speed = (demand_x - (demand_z * 0.190)) / 0.01666
    r_speed = (demand_x + (demand_z * 0.190)) / 0.01666

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("cmd_vel", Twist, cmd_vel_cb)


def driveMotor(motor, speed_right, speed_left):

    vel_r_low = speed_right & 0xff
    vel_r_high = speed_right >> 8 & 0xff

    vel_l_low = speed_left & 0xff
    vel_l_high = speed_left >> 8 & 0xff

    buffer = [0,0,0,0,0,0,0,0,0,0,0]            #tbh idk wtf
    buffer[0] = motor
    buffer[1] = 0x10
    buffer[2] = 0x20
    buffer[3] = 0x88
    buffer[4] = 0x00
    buffer[5] = 0x02
    buffer[6] = 0x04
    buffer[7] = vel_l_high
    buffer[8] = vel_l_low
    buffer[9] = vel_r_high
    buffer[10] = vel_r_low
    crc = libscrc.modbus(bytearray(buffer))
    buffer.extend([0, 0])
    buffer[11] = crc & 0xff
    buffer[12] = crc >> 8 & 0xff

    ser.write(buffer)
    time.sleep(0.05)

if __name__ == '__main__':
    listener()

while not rospy.is_shutdown():
    driveMotor(1, int(r_speed * -1), int(l_speed))
    serialRx()
    driveMotor(2, int(r_speed * -1), int(l_speed))
    serialRx()
