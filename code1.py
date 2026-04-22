import serial
import paho.mqtt.client as mqtt
import time

# Port série Arduino
SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600

# Configuration HiveMQ
BROKER = "d186cc1940054fa9aed773820d682ed1.s1.eu.hivemq.cloud"
PORT = 8883
TOPIC = "moniot/luminosite"
CLIENT_ID = "Raspberry_LDR"
CLIENT_USERNAME = "groupe3"
CLIENT_PASSWORD = "Ioti2026"

# Connexion
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    client = mqtt.Client(CLIENT_ID)
    client.username_pw_set(CLIENT_USERNAME, CLIENT_PASSWORD)
    client.tls_set()  # ← important pour port 8883 !
    client.connect(BROKER, PORT, 60)
except Exception as e:
    print(f"Erreur connexion : {e}")
    exit()

# Envoi données
try:
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            print(f"Luminosité : {data}")
            client.publish(TOPIC, data)
        time.sleep(1)
except KeyboardInterrupt:
    print("Arrêt.")
finally:
    ser.close()
    client.disconnect()
