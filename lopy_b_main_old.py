#v2 RP 28Dec2020
from network import LoRa
import socket
import machine
import time
from machine import Pin
import pycom
import ustruct
import ubinascii

# from https://github.com/MZachmann/oled-python-library
from graphicslib import OledGrafx
##from graphicslib import OledDisplay
# False for SH1103
x = OledGrafx.OledGrafx(False)
#d = OledGrafx.OledDisplay(False)
x.PrintStrings("Waking up","...","Hello from lopy-b")
time.sleep(1)
x.oled.clear()

COLOUR_WHITE = 0xFFFFFF
COLOUR_BLACK = 0x000000
COLOUR_RED   = 0xFF0000
COLOUR_GREEN = 0x00FF00
COLOUR_BLUE  = 0x0000FF

CMD_ON="Sophie"
CMD_OFF="Milly"

solenoid_state="GREEN"
# cCMD_ON=ustruct.pack('s', CMD_ON)
# cCMD_OFF=ustruct.pack('s',CMD_OFF)
# bCMD_ON=ubinascii.b2a_base64(cCMD_ON)
# aCMD_ON=ubinascii.a2b_base64(bCMD_ON)
# print("CMD_ON ", CMD_ON, " char ", cCMD_ON, " bin ", bCMD_ON, " asc ", aCMD_ON  )
# print("CMD_OFF ", CMD_OFF, " bin ", bCMD_OFF)
pycom.heartbeat(False)
pycom.rgbled(COLOUR_WHITE)
print("---")
#print("Unpacked value is:", ustruct.unpack('s',bCMD_ON)[0])
# print("Unpacked value is:", ustruct.unpack('s',bCMD_OFF))

#p_outG16 = Pin('G16', mode=Pin.OUT)
## relay pins
p_outG22 = Pin('G22', mode=Pin.OUT)  #in2
p_outG28 = Pin('G28', mode=Pin.OUT)  #in1
#turn off solenoids
p_outG22.value(1)
p_outG28.value(1)

## momentary switch input pins
p_inG12 = Pin('G12', mode=Pin.IN, pull=Pin.PULL_UP)
p_inG13 = Pin('G13', mode=Pin.IN, pull=Pin.PULL_UP)

i=0
s_rssi="nothing"
s_snr="nothing"
s_freq="nothing"
#from https://docs.pycom.io/tutorials/lora/lora-mac/ and on https://www.youtube.com/watch?v=CXZCbTif1Ns

# initialise LoRa in LORA mode
# Asia = LoRa.AS923
# Australia = LoRa.AU915
#lora = LoRa(mode=LoRa.LORA, region=LoRa.AU915)
### lora = LoRa(mode=LoRa.LORA, region=LoRa.AU915, sf=7, tx_power=19, power_mode=LoRa.ALWAYS_ON)
lora = LoRa(mode=LoRa.LORA, rx_iq=True, region=LoRa.AU915)
# create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)
print ("starting lopy-b")
print(lora.frequency())

# send some data
## s.setblocking(True)
s.send("Hi from lopy b")
while True:
 i=i+1
 if p_inG12.value()==0:
    solenoid_state="GREEN"
    print("manual set to ", solenoid_state)
 elif  p_inG13.value()==0:
	solenoid_state="BLUE"
	print("manual set to ", solenoid_state)
 if solenoid_state=="GREEN":
    p_outG22.value(1)
    p_outG28.value(0)
    pycom.rgbled(COLOUR_GREEN)
    time.sleep_ms(200)
    pycom.rgbled(COLOUR_BLACK)
 else:
    p_outG22.value(0)
    p_outG28.value(1)
    pycom.rgbled(COLOUR_BLUE)
    time.sleep_ms(200)
    pycom.rgbled(COLOUR_BLACK)
 x.oled.clear()
 x.PrintStrings(str(i), "solenoid: ",solenoid_state)
 # get any data received...
 s.setblocking(False)
 rcv_data = s.recv(64)
 if rcv_data:
    print(i, "rcv_data ",rcv_data)
    print(i, "len(rcv_data) ",len(rcv_data))
    print(i, "type(rcv_data) ",type(rcv_data))
    try:
        rcv_data1=rcv_data.decode("utf-8")
    except:
        print("decode on error")
        rcv_data1="dummy"

    print(i, "rcv_data1 ",rcv_data)
    print(i, "len(rcv_data1) ",len(rcv_data))
    print(i, "type(rcv_data1) ",type(rcv_data))
    s_rssi="rssi: " + str(lora.stats()[1])
    s_snr="snr: " + str(lora.stats()[2])
    s_freq="f: " + str(lora.stats()[9]/1000000)
    print(s_rssi, s_snr, s_freq)
    x.oled.clear()
    x.PrintStrings(str(i) + " new data:",s_rssi,s_snr,s_freq)
    if rcv_data1==CMD_ON:
        print("rcv_data==CMD_ON", rcv_data1 )
        solenoid_state="GREEN"
        s.setblocking(True)
        s.send(CMD_ON)
        s.setblocking(False)
    elif rcv_data1==CMD_OFF:
        print("rcv_data==CMD_OFF", rcv_data1)
        solenoid_state="BLUE"
        s.setblocking(True)
        s.send(CMD_OFF)
        s.setblocking(False)
    else:
        print("Unknown lora message received: ", rcv_data,rcv_data1, s_rssi, s_snr, s_freq )
 else:
    print(solenoid_state, " no data received; last rssi ", s_rssi)
    x.oled.clear()
    x.PrintStrings("   last values:",s_rssi,s_snr,s_freq)
    # wait a random amount of time
time.sleep(3)
if i==1024:
 i=0
