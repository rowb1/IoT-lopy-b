### RP 29 DEC 20 Gateway -- https://forum.pycom.io/topic/4110/first-contact-with-lora-no-success/7

import socket
import struct
from network import LoRa#, WLAN
import machine
#import config

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
    print("Done!!!")
    print("Init LoRa socket...", end='')
    lora_sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    print("Done!!!")
    print("Disable LoRa blocking...", end='')
    lora_sock.setblocking(False)
    print("Done!!!")
    print("Ready to receive LoRa packets")
    print(lora.frequency())


start_lora()

while (True):
    recv_pkg = lora_sock.recv(512)
    print(recv_pkg)
    if (len(recv_pkg) > 2):
        print(recv_pkg[1])
        recv_pkg_len = recv_pkg[1]

        device_id, pkg_len, msg = struct.unpack(_LORA_PKG_FORMAT % recv_pkg_len, recv_pkg)

        # If the uart = machine.UART(0, 115200) and os.dupterm(uart) are set in the boot.py this print should appear in the serial port
        print('Device: %d - Pkg:  %s' % (device_id, msg))

        ack_pkg = struct.pack(_LORA_PKG_ACK_FORMAT, device_id, 1, 200)
        lora_sock.send(ack_pkg)
        print("ACK send")
    time.sleep_ms(1100)
