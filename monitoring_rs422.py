import serial
import struct
import time
from collections import deque

PORT = 'COM6'  # ou '\\\\.\\COM10'
BAUDRATE = 19200

last_time = None
intervals = deque(maxlen=10)  # stocke les 10 derniers intervalles

def calculate_checksum(data):
    checksum = 0
    for byte in data:
        checksum ^= byte
    return checksum

try:
    with serial.Serial(port= PORT, baudrate= BAUDRATE, timeout=1, parity= serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE) as ser:
        print(f"Lecture du port {PORT} à {BAUDRATE} bauds", flush=True)
        buffer = bytearray()
        while True:
            byte = ser.read(1)
            if not byte:
                continue
            b = byte[0]
            #print(b)  
            print(f"{b:02X}")
            

except serial.SerialException as e:
    print(f"Erreur d'accès au port: {e}", flush=True)
