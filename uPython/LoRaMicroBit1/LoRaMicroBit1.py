# LoRaMicroBit 1
# Send text string to TTN using the RTC timer every 10 minutes

# RN2483 LoRaMicro:Bit V1.0
from microbit import *

# Device Specific definitions
# Update these when you register device to The Things Network
app_eui = "70B3D57ED000061F"
dev_eui = "0004A30B001ACADD"
app_key = "FB54C5126274030C482735696B8815E9"

#global variables
program_phase = 0
program_state = 0
debug_led_enable = True

#Phase 0 Initialise Hardware
def hw_init():
    global program_phase
    global program_state
    display.clear() # clear display
    display.set_pixel(program_phase, program_state, 5) # update status
    program_state = 1
    clear_time()
    display.set_pixel(program_phase, program_state, 5) # update status
    program_state = 2
 
    pin16.write_digital(1) # hold power on
    pin2.write_digital(1) # RN2483 reset high

    display.set_pixel(program_phase, program_state, 5) # update status
    program_phase = 1 # phase 0 complete
    program_state = 0 # reset state
 
 
#Phase 1 Collect Data to send
def collect_data():
    global program_phase
    global program_state
    display.set_pixel(program_phase, program_state, 5) # update status
    
    
    program_state = 1
    display.set_pixel(program_phase, program_state, 5) # update status
    program_phase = 2 # phase 1 complete
    program_state = 0 # reset state
    return(b"BBC Micro:Bit Timer")
  
#Phase 2 Initalise Radio   
def init_radio():
    global program_phase
    global program_state
    display.set_pixel(program_phase, program_state, 5) # update status
    program_state = 1
    
    RN2483_Reset() # Reset RN2483
 
    RN2483_SendCommand("mac set appeui %s\r\n" % app_eui)
    RN2483_SendCommand("mac set deveui %s\r\n" % dev_eui)
    RN2483_SendCommand("mac set appkey %s\r\n" % app_key)
    RN2483_SendCommand("mac join otaa\r\n")
    response = RN2483_CheckResponse()
 

    display.set_pixel(program_phase, program_state, 5) # update status
    program_phase = 3 # phase 2 complete
    program_state = 0 # reset state  

#Phase 3 Send data and get reply
def send_data(data):
    global program_phase
    global program_state
    display.set_pixel(program_phase, program_state, 5) # update status
    program_state = 1
    
    RN2483_SendData(data)
    response = RN2483_CheckResponse()
    uart.init(115200)
    print(response)

    display.set_pixel(program_phase, program_state, 5) # update status
    program_phase = 3 # phase 2 complete
    program_state = 0 # reset state  


#Phase 4 Set alarm for wake up
    
def set_alarm(Hours, Mins, Secs):
 
    tens, units = divmod(Secs, 10)
    BCD_Secs = (tens <<4) + units
    tens, units = divmod(Mins,10)
    BCD_Mins = (tens <<4) + units
    tens, units = divmod(Hours,10)
    BCD_Hours = (tens <<4) + units
    
    Registers = bytearray([0x0A, BCD_Secs, BCD_Mins, BCD_Hours, 0x70, 0x00, 0x00])
    i2c.write (0x6F, Registers)
 
def clear_time():
    Registers = bytearray([0x00, 0x80, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x10])
    i2c.write (0x6F, Registers)

def RN2483_Reset(): # Reset RN2483
    uart.init(57600,tx=pin12,rx=pin8 )
    pin2.write_digital(1)
    pin2.write_digital(0)
    pin2.write_digital(1)
    response_string = RN2483_CheckResponse()
    return response_string


def RN2483_SendCommand(command):
    uart.write(command)
    response_string = RN2483_CheckResponse()
    return response_string

def RN2483_CheckResponse():

    for i in range(100):
        sleep(100)
        if uart.any():
            break
    response_string = uart.readline()
    return response_string

def RN2483_SendData(data):
    uart.write("mac tx uncnf 1 ")
    for char in data:
        nibble = char >> 4
        if nibble > 9:
            nibble = nibble + 0x37
        else:
            nibble = nibble + 0x30
        uart.write(chr(nibble))
        nibble = char & 0x0f
        if nibble > 9:
            nibble = nibble + 0x37
        else:
            nibble = nibble + 0x30
        uart.write(chr(nibble))
    uart.write("\r\n")
    #RN2483_CheckResponse()
    response_string = RN2483_CheckResponse()
    return response_string

def Power_Off():
    pin16.write_digital(0)

# Start Here   


hw_init() # phase 0
lora_data_bytes = collect_data() # phase 1
init_radio() # phase 2
send_data(lora_data_bytes) # phase 3 send the data to LoRaWAN
set_alarm(0,10,0) # phase 4 set alarm time (hr,min,sec)
Power_Off()
