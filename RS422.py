import serial
import struct
import time
from collections import deque

PORT = '\\\\.\\COM10'  # ou '\\\\.\\COM10'
BAUDRATE = 9600

last_time = None
intervals = deque(maxlen=10)  # stocke les 10 derniers intervalles

def calculate_checksum(data):
    checksum = 0
    for byte in data:
        checksum ^= byte
    return checksum

try:
    with serial.Serial(PORT, BAUDRATE, timeout=1) as ser:
        print(f"Lecture du port {PORT} à {BAUDRATE} bauds", flush=True)
        buffer = bytearray()
        while True:
            byte = ser.read(1)
            if not byte:
                continue
            b = byte[0]

            if len(buffer) == 0:
                if b == 0x64:  # Début de trame
                    buffer.append(b)
            else:
                buffer.append(b)
            # Météo
            # if len(buffer) >= 3 and len(buffer) == buffer[2] + 1: #trame entièrement recue 
            #     if buffer[1] == 0x02:  # ID météo
            #         data = buffer[:26]            # sans le checksum
            #         received_checksum = buffer[26]
            #         computed_checksum = calculate_checksum(data)
            #         if received_checksum == computed_checksum:
            #             temp_signed = struct.unpack(">h", buffer[9:11])[0]
            #             temp_celsius = temp_signed / 16.0
                        
            #             heure = buffer[23]
            #             minute = buffer[24]
            #             seconde = buffer[25]
            
            #             print(f"Température : {temp_celsius:.2f} °C", flush=True)
            #             print(f"Heure UTC : {heure:02}:{minute:02}:{seconde:02}", flush=True)
            #         else: 
            #             print(f"Checksum invalide !")
            #     buffer.clear()
                             
            # Angle 
            if len(buffer) >= 3 and len(buffer) == buffer[2] + 1:  # trame entièrement reçue
                if buffer[1] == 0x01:  # ID centrale inertielle
                    data = buffer[:buffer[2]]
                    received_checksum = buffer[buffer[2]]
                    computed_checksum = calculate_checksum(data)
                    if received_checksum == computed_checksum:
                        current_time = time.time()
                        if last_time is not None:
                            dt = current_time - last_time
                            intervals.append(dt)
                            if len(intervals) >= 2:
                                avg_interval = sum(intervals) / len(intervals)
                                avg_freq = 1.0 / avg_interval
                                #print(f"Fréquence moyenne : {avg_freq:.2f} Hz", flush=True)
                        last_time = current_time
                        angle_site = struct.unpack(">b", buffer[3:4])[0]  # int8 signé
                        print(f"Angle de site : {angle_site} °", flush=True)
                    else:
                        print("Checksum invalide !", flush=True)
                buffer.clear()

except serial.SerialException as e:
    print(f"Erreur d'accès au port: {e}", flush=True)
