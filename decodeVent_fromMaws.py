import serial
import struct

PORT = 'COM10'  # adapte selon ton système
BAUDRATE = 9600
TIMEOUT = 1  # secondes

def calculate_checksum(data):
    checksum = 0
    for b in data:
        checksum ^= b
    return checksum

def decode_vent_hcgpse(frame):
    if len(frame) != 38:
        return None

    data = frame[:37]
    received_checksum = frame[37]
    computed_checksum = calculate_checksum(data)

    if received_checksum != computed_checksum:
        print("❌ Checksum invalide")
        return None

    # Octets 6-7 : vitesse (big endian), Octets 8-9 : direction (big endian)
    vitesse_raw = struct.unpack(">h", bytes(data[5:7]))[0]
    direction_raw = struct.unpack(">h", bytes(data[7:9]))[0]

    vitesse = vitesse_raw / 16.0  # m/s
    direction = direction_raw / 16.0  # degrés

    return vitesse, direction

# === Boucle principale ===
try:
    with serial.Serial(PORT, BAUDRATE, timeout=TIMEOUT, parity=serial.PARITY_EVEN) as ser:
        print(f"📡 Lecture trames MAWS5000 HCGPSE sur {PORT}...\n")
        buffer = bytearray()

        while True:
            byte = ser.read(1)
            if not byte:
                continue

            b = byte[0]

            if len(buffer) == 0:
                if b == 85:  # Début de trame
                    buffer.append(b)
            else:
                buffer.append(b)

            if len(buffer) >= 2 and len(buffer) == buffer[1] + 2:  # longueur OK
                result = decode_vent_hcgpse(buffer)
                if result:
                    vitesse, direction = result
                    print(f" Vitesse : {vitesse:.2f} m/s | Direction : {direction:.1f}°")
                buffer.clear()

except serial.SerialException as e:
    print(f"⚠ Erreur série : {e}")
