from network import LoRa
import socket
import machine
import time
from machine import Pin
import pycom
import ustruct
import ubinascii

# from https://github.com/MZachmann/oled-python-library
##from graphicslib import OledGrafx
##from graphicslib import OledDisplay
# False for SH1103
##x = OledGrafx.OledGrafx(False)
#d = OledGrafx.OledDisplay(False)
##x.PrintStrings("Waking up","...","Hello","lora")
##time.sleep(1)
##x.oled.clear()

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
p_outG22 = Pin('G22', mode=Pin.OUT)
p_outG28 = Pin('G28', mode=Pin.OUT)

p_in = Pin('P10', mode=Pin.IN, pull=Pin.PULL_UP)
i=0
s_rssi="nothing"
s_snr="nothing"
s_freq="nothing"
#from https://docs.pycom.io/tutorials/lora/lora-mac/ and on https://www.youtube.com/watch?v=CXZCbTif1Ns

# initialise LoRa in LORA mode
# Asia = LoRa.AS923
# Australia = LoRa.AU915
lora = LoRa(mode=LoRa.LORA, region=LoRa.AS923, sf=7)
# create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
print ("starting up ... B")
p_outG22.value(0)
p_outG28.value(0)

# send some data
s.setblocking(True)
s.send("Hi from B")
print(i, "B message sent")

while True:
    i=i+1

    if solenoid_state=="GREEN":
        pycom.rgbled(COLOUR_GREEN)
        time.sleep_ms(200)
        pycom.rgbled(COLOUR_BLACK)
    else:
        pycom.rgbled(COLOUR_BLUE)
        time.sleep_ms(200)
        pycom.rgbled(COLOUR_BLACK)

    ##x.PrintStrings(str(i))
    ##time.sleep(1)
    ##x.oled.clear()
    # send some data
    #s.setblocking(True)
    #s.send("Hi from B")
    #print(i, "B message sent")

    #print(i, 'push button',p_in.value())
# print('toggle sw', p_in2.value())
#set expansion board button to light expansion board LED
    #p_outG16(p_in.value())
    ##inteferes with 12c
    #p_outG22(p_in.value())
    #p_outG28(p_in.value())


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
        ##x.PrintStrings(str(i) + " new data:",s_rssi,s_snr,s_freq)

        if rcv_data1==CMD_ON:
            print("rcv_data==CMD_ON", rcv_data1 )
            solenoid_state="GREEN"
            s.send(CMD_ON)
            pycom.rgbled(COLOUR_GREEN)
            time.sleep_ms(400)
            pycom.rgbled(COLOUR_BLACK)
            p_outG22.value(1)
            p_outG28.value(0)

        elif rcv_data1==CMD_OFF:
            print("rcv_data==CMD_OFF", rcv_data1)
            solenoid_state="BLUE"
            s.send(CMD_OFF)
            pycom.rgbled(COLOUR_BLUE)
            time.sleep_ms(400)
            pycom.rgbled(COLOUR_BLACK)
            p_outG22.value(0)
            p_outG28.value(1)
        else:
            print("Outsider: ", rcv_data, s_rssi, s_snr, s_freq )
            print(CMD_ON, CMD_OFF)
    else:
        print("nothing new; last ", s_rssi)
        ##x.PrintStrings("   last values:",s_rssi,s_snr,s_freq)

    # wait a random amount of time

    time.sleep(4)
    if i==1024:
        i=0
