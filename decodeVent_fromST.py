import serial
import struct

PORT = '\\\\.\\COM10'  # ou '\\\\.\\COM10'
BAUDRATE = 9600


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
            #Météo
            if len(buffer) >= 3 and len(buffer) == buffer[2] + 1: #trame entièrement recue 
                if buffer[1] == 0x02:  # ID météo
                    data = buffer[:26]            # sans le checksum
                    received_checksum = buffer[26]
                    computed_checksum = calculate_checksum(data)
                    if received_checksum == computed_checksum:
                        #Todo
                        # Décodage des 2 vitesses en complément à 2, big endian
                        v_face_raw = struct.unpack('>h', data[6:8])[0]
                        v_travers_raw = struct.unpack('>h', data[8:10])[0]

                        # Conversion avec résolution de 1/16
                        v_face_mps = v_face_raw / 16.0
                        v_travers_mps = v_travers_raw / 16.0
                        print(f"Vent de face : {v_face_mps:.2f} m/s, Vent de travers : {v_travers_mps:.2f} m/s")

                    else: 
                        print(f"Checksum invalide !")
                buffer.clear()
                             
           

except serial.SerialException as e:
    print(f"Erreur d'accès au port: {e}", flush=True)
