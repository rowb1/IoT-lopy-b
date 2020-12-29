### RP 29 DEC 20 Gateway -- https://forum.pycom.io/topic/4110/first-contact-with-lora-no-success/7
### RP add LEDS - try 2, minimal
import socket
import struct
from network import LoRa
import machine
import time
from graphicslib import OledGrafx
import pycom

x = OledGrafx.OledGrafx(False)
COLOUR_BLACK = 0x000000
COLOUR_RED   = 0xFF0000
COLOUR_GREEN = 0x00FF00
COLOUR_BLUE  = 0x0000FF
pycom.heartbeat(False)
pycom.rgbled(COLOUR_BLACK)

# A basic package header, B: 1 byte for the deviceId, B: 1 byte for the pkg size, %ds: Formated string for string
_LORA_PKG_FORMAT = "!BB%ds"
# A basic ack package, B: 1 byte for the deviceId, B: 1 bytes for the pkg size, B: 1 byte for the Ok (200) or error messages
_LORA_PKG_ACK_FORMAT = "BBB"


lora = None
lora_sock = None

def start_lora():
    global lora
    global lora_sock

    print("Init LoRa radio...", end='')
    lora = LoRa(mode=LoRa.LORA, rx_iq=True, region=LoRa.AU915)
    print("Init LoRa socket...", end='')
    lora_sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    lora_sock.setblocking(False)
    print("Ready to receive LoRa packets")
    print(lora.frequency())

def start_OLED():
    x.PrintStrings("Waking up","...","Lopy-b says hello")
    time.sleep(1)
    x.oled.clear()
    x.PrintStrings("freq:= ", str(lora.frequency()))
    time.sleep(1)
#    x.oled.clear()

def printLoraStats():
    s_rssi="rssi: " + str(lora.stats()[1])
    s_snr="snr: " + str(lora.stats()[2])
    s_freq="f: " + str(lora.stats()[9]/1000000)
    print(s_rssi, s_snr, s_freq)
    x.oled.clear()
    x.PrintStrings(s_rssi,s_snr,s_freq)
    time.sleep_ms(1000)

start_lora()
start_OLED()

while (True):
    msg=""
    recv_pkg = lora_sock.recv(512)
    ##print(recv_pkg)
    if (len(recv_pkg) > 2):
        ##print(recv_pkg[1])
        recv_pkg_len = recv_pkg[1]
        printLoraStats()
        device_id, pkg_len, msg = struct.unpack(_LORA_PKG_FORMAT % recv_pkg_len, recv_pkg)
        x.oled.clear()
        x.PrintStrings('%s' % (msg))
        # If the uart = machine.UART(0, 115200) and os.dupterm(uart) are set in the boot.py this print should appear in the serial port
        print('Device: %d - Pkg:  %s' % (device_id, msg))
        #print('msg type:', type(msg))
        #print(msg[5])
        ack_pkg = struct.pack(_LORA_PKG_ACK_FORMAT, device_id, 1, 200)
        lora_sock.send(ack_pkg)
        print("ACK send")
    time.sleep_ms(1100)
