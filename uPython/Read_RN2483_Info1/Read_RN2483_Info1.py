# Read_RN2483_Info1
# Read the Version number an the HWEUI from RN2483

# RN2483 LoRaWAN
from microbit import *

def RN2483_Reset(): # Reset RN2483
    uart.init(57600,tx=pin12,rx=pin8 )
    pin2.write_digital(1)
    pin2.write_digital(0)
    pin2.write_digital(1)
    RN2483_GetResponse()
    
def RN2483_SendCommand(command):
    uart.write(command)
    response_string = RN2483_GetResponse()
    return response_string
def RN2483_GetResponse():
    
    for i in range(100):
        sleep(100)
        if uart.any():
            break
    response_string = uart.readline()
    return response_string


RN2483_Reset()
#RN2483_SendCommand("sys factoryRESET\r\n")
response_ver = RN2483_SendCommand("sys get ver\r\n")
response_hweui = RN2483_SendCommand("sys get hweui\r\n")

uart.init(115200)
uart.write("\r\nSoftware Version =")
uart.write(response_ver)
uart.write("\r\nFixed Hardware EUI =")
uart.write(response_hweui)





while True:

    sleep(1000)
    
