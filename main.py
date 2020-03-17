#lopy- copied over from Grushenka
from network import LoRa
import socket
import machine
import time
from machine import Pin
import pycom

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
#from https://docs.pycom.io/tutorials/lora/lora-mac/ and on https://www.youtube.com/watch?v=CXZCbTif1Ns

# initialise LoRa in LORA mode
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
# more params can also be given, like frequency, tx power and spreading factor
lora = LoRa(mode=LoRa.LORA, region=LoRa.AU915, sf=7)

# create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
print ("starting up ... B")

while True:
    i=i+1
    # send some data
    s.setblocking(True)
    s.send("Hi from B")
    #print(i, "B message sent")

    #print(i, 'push button',p_in.value())
# print('toggle sw', p_in2.value())
    p_outG16(p_in.value())
    #p_outG22(p_in.value())
    #p_outG28(p_in.value())


    # get any data received...
    s.setblocking(False)
    rcv_data = s.recv(64)
    if rcv_data:
        print(i, "rcv_data ",rcv_data)
        print(i, "rcv_data[0] ",rcv_data[0])
        print(i,"bytes(rcv_data[0]) ", bytes(rcv_data[0]))
        stats_tuple=lora.stats()
        print(i, "rssi: ", stats_tuple[1], "freq: ", stats_tuple[9])

        if rcv_data[0]:
            pycom.rgbled(COLOUR_GREEN)
            p_outG22.value(1)
        else:
            pycom.rgbled(COLOUR_BLUE)
            p_outG22.value(0)

    # wait a random amount of time

    time.sleep(1)
    if i==1024:
        i=0

