#lopy- copied over from Grushenka
from network import LoRa
import socket
import machine
import time
from machine import Pin
import pycom

# from https://github.com/MZachmann/oled-python-library
from graphicslib import OledGrafx
from graphicslib import OledDisplay
# False for SH1103
x = OledGrafx.OledGrafx(False)
#d = OledGrafx.OledDisplay(False)
x.PrintStrings("Waking up","...","Hello","lora")
time.sleep(1)
x.oled.clear()

time.sleep(1)
#x.PrintStrings("100",str(200),"300","400")
COLOUR_WHITE = 0xFFFFFF
COLOUR_BLACK = 0x000000
COLOUR_RED   = 0xFF0000
COLOUR_GREEN = 0x00FF00
COLOUR_BLUE  = 0x0000FF

pycom.heartbeat(False)
pycom.rgbled(COLOUR_BLACK)

p_outG16 = Pin('G16', mode=Pin.OUT)
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
p_outG28.value(0)

# send some data
s.setblocking(True)
s.send("Hi from B")
print(i, "B message sent")

while True:
    i=i+1
    x.PrintStrings(str(i))
    time.sleep(1)
    x.oled.clear()
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
    #    print(i, "rcv_data[0] ",rcv_data[0])
    #    print(i,"bytes(rcv_data[0]) ", bytes(rcv_data[0]))
        s_rssi="rssi: " + str(lora.stats()[1])
        s_snr="snr: " + str(lora.stats()[2])
        s_freq="f: " + str(lora.stats()[9]/1000000)
        print(s_rssi, s_snr, s_freq)
        x.PrintStrings(str(i) + " new data:",s_rssi,s_snr,s_freq)
        if rcv_data[0]:
            pycom.rgbled(COLOUR_GREEN)
            p_outG22.value(1)
            p_outG28.value(0)
        else:
            pycom.rgbled(COLOUR_BLUE)
            p_outG22.value(0)
            p_outG28.value(1)
    else:
        print("nothing new; last ", s_rssi)
        x.PrintStrings("   last values:",s_rssi,s_snr,s_freq)

    # wait a random amount of time

    time.sleep(4)
    if i==1024:
        i=0
