# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 10:37:11 2019

@author: McLaren
"""


import serial
import time
 
ser = serial.Serial()
 
def port_open(port_no):
    ser.port = port_no      #设置端口号
    ser.baudrate = 9600     #设置波特率
    ser.bytesize = 8        #设置数据位
    ser.stopbits = 1        #设置停止位
    ser.parity = "N"        #设置校验位
    ser.open()              #打开串口,要找到对的串口号才会成功
    if(ser.isOpen()):
        print("串口打开成功")
    else:
        print("串口打开失败")
 
def port_close():
    ser.close()
    if (ser.isOpen()):
        print("串口关闭失败")
    else:
        print("串口关闭成功")
 
def send(Position0,Position1):
    if (ser.isOpen()):
        Position0=round(Position0*100/1080)    #像素转百分比
        Position1=round(Position1*100/607)
        if Position0<16:                       #如果数据不满一个字节补零
            Position0 = '0'+hex(Position0)[2:]
        else:
            Position0 = hex(Position0)[2:]
        if Position1<16:
            Position1 = '0'+hex(Position1)[2:]
        else:
            Position1 = hex(Position1)[2:]    
            
        send_data = Position0+Position1+'FF'
        #ser.write(send_data.encode('utf-8'))  #utf-8 编码发送
        ser.write(bytes.fromhex(send_data))  #Hex发送
        #print("发送成功",send_data)
    else:
        print("发送失败",'像素位置：{}%,{}%'.format(round(Position0*100/1080),round(Position1*100/607)))

def wait_for_flag():
    time.sleep(1)     #sleep() 与 inWaiting() 最好配对使用
    num=ser.inWaiting()
    torient_time = 0
    while True:
        torient_time+=1
        if (ser.read(num)==b'\xff')or(torient_time==25):
            break              #收到0xFF或25秒没收到(可能数据丢包)都跳出
        else:
            time.sleep(1)
            num=ser.inWaiting()
    #time.sleep(1)
#bytes.fromhex(hex(99)[2:])

