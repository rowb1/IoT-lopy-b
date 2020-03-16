from network import LoRa
import socket
import machine
import time
from machine import Pin
import pycom

COLOUR_BLUE  = 0x0000FF
COLOUR_BLACK = 0x000000
#from https://docs.pycom.io/tutorials/lora/lora-mac/ and on https://www.youtube.com/watch?v=CXZCbTif1Ns

# initialise LoRa in LORA mode
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# more params can also be given, like frequency, tx power and spreading factor
p_inG10 = Pin('G10', mode=Pin.IN, pull=Pin.PULL_UP)
p_outLED = Pin('G16', mode=Pin.OUT)
oldToggleState=p_inG10.value()
i=0

lora = LoRa(mode=LoRa.LORA, region=LoRa.AS923, sf=7, tx_power=19)
lora.frequency(927200000)
# create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
print ("starting up ... A")

s.send("Hello from A")
print("sent Hello from A")

while True:
    i=i+1
    if not p_inG10.value() == oldToggleState:
        #print("toggle value changed")
        print(i,' toggle sw :',p_inG10.value())
        s.setblocking(True)
        if p_inG10.value()==0:
            p_outLED.value(1)
            s.send(bytes([0x00]))
            print("0x00 sent")
        else:
			p_outLED.value(0)
			# turn inbuilt LED on
			s.send(bytes([0x11]))
			print("0x11 sent")
    #else:
        #print("toggle has not changed")
    # get any data received...
    s.setblocking(False)
    rcv_data = s.recv(64)
    if rcv_data:
        stats_tuple=lora.stats()
        print(i, "rssi: ", stats_tuple[1], "freq: ", stats_tuple[9])
        print(data)
    oldToggleState=p_inG10.value()
    if i==1024:
        i=0
    # wait a random amount of time
    #time.sleep(machine.rng() & 0x0F)
    time.sleep(1)
