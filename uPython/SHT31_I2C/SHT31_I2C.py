#
# SHT31 I2C test
# Read  external I2C temperature humidity sensor
from microbit import *

def ReadStatus():
    sbuf = bytearray([0xF3, 0x2D])
    i2c.write (0x44, sbuf)
    return i2c.read(0x44,3)
    
def ClearStatus():
    sbuf = bytearray([0x30, 0x41])
    i2c.write (0x44, sbuf)
    
def ReadTempHum():
    sbuf = bytearray([0x24, 0x00])
    i2c.write (0x44, sbuf)
    sleep(500)
    return i2c.read(0x44,6)
    

print("\r\n")  
print(ReadStatus())
ClearStatus()
print(ReadStatus())
print(":".join("{:02x}".format(c) for c in ReadStatus()))
TempHum = ReadTempHum()
print(":".join("{:02x}".format(c) for c in TempHum))
Temperature = (((TempHum[0] << 8) + TempHum[1]) * 175 / 65535) -45
print("Temperature = %2.2f degrees" % Temperature)
Humidity = ((TempHum[3] << 8) + TempHum[4]) * 100 / 65535
print("Humidity = %2.2f percent" % Humidity)
