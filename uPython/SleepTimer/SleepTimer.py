# SleepTimer.py
# Test the rtc timer works

from microbit import *
def Power_On():
    pin8.write_digital(1)
def Power_Off():
    pin8.write_digital(0)
    
def MCP7940_Set_Alarm(Hours, Mins, Secs):
    tens, units = divmod(Secs, 10)
    BCD_Secs = (tens <<4) + units
    tens, units = divmod(Mins,10)
    BCD_Mins = (tens <<4) + units
    tens, units = divmod(Hours,10)
    BCD_Hours = (tens <<4) + units
    
    Registers = bytearray([0x0A, BCD_Secs, BCD_Mins, BCD_Hours, 0x70, 0x00, 0x00])
    i2c.write (0x6F, Registers)
    Registers = bytearray([0x00, 0x80, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x10])
    i2c.write (0x6F, Registers)

def MCP7940_Check_Alarm():
    address = bytearray([0x0d])
    i2c.write (0x6F, address)
    Alarm = i2c.read( 0x6f,1)
    return Alarm[0]
    
    
def MCP7940_ReadClock():
    address = bytearray([0x00])
    i2c.write (0x6F, address)
    ClockData = i2c.read(0x6F,7)
    SecLSB = ClockData[0] & 0x0f
    SecMSB = (ClockData[0] & 0x70) >> 4
    Seconds = (SecMSB * 10) + SecLSB
    MinLSB = ClockData[1] & 0x0f
    MinMSB = (ClockData[1] & 0x70) >> 4
    Minutes = (MinMSB * 10) + MinLSB
    HrLSB = ClockData[2] & 0x0f
    HrMSB = (ClockData[2] & 0x30) >> 4
    Hours = (HrMSB * 10) + HrLSB
    Day = ClockData[3] & 0x07
    DateLSB = ClockData[4] & 0x0f
    DateMSB = (ClockData[4] & 0x30) >> 4
    Date =(DateMSB * 10) + DateLSB
    MonLSB = ClockData[5] & 0x0f
    MonMSB = (ClockData[5] & 0x10) >> 4
    Month =(MonMSB * 10) + MonLSB
    YrLSB = ClockData[6] & 0x0f
    YrMSB = (ClockData[6] & 0xf0) >> 4
    Year =(YrMSB * 10) + YrLSB
    return(Year, Month, Date, Day, Hours, Minutes, Seconds)


sDay = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
sMonth = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
Power_On()
display.show(Image.NO)
MCP7940_Set_Alarm(0,1,0)
Power_Off()
while True:
    (Year, Month, Date, Day, Hours, Minutes, Seconds) = MCP7940_ReadClock()
    print("Time is %d:%d:%d %s %d %s %d" % (Hours, Minutes, Seconds, sDay[Day], Date, sMonth[Month], Year + 2000))
    Alarm = MCP7940_Check_Alarm()
    print("Alarm %x" % (Alarm))
    if(Alarm == 0x78):
        display.show(Image.NO)
    sleep(5000)
    Power_Off()

