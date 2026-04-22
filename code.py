import serial
import paho.mqtt.client as mqtt
import time

SERIAL_PORT = "/dev/ttyACM0" # Your Arduino port
BAUD_RATE = 9600

# We are using a public, free broker for this TP
BROKER = "mqtt.eclipseprojects.io" 
PORT = 1883
TOPIC = "fstt/student/luminosite" # PRO TIP: Change this to something unique!
CLIENT_ID = "Raspberry_LDR_Tangier"

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    client = mqtt.Client(CLIENT_ID)
    client.connect(BROKER, PORT, 60)
    print("Connected to Broker!")
except Exception as e:
    print(f"Connection Error: {e}")
    exit()

try:
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            print(f"Sending to MQTT: {data}")
            # This line sends the data to the cloud post office
            client.publish(TOPIC, data)
            time.sleep(1) # Wait 1 second between sends
except KeyboardInterrupt:
    print("Stopping...")
finally:
    ser.close()
    client.disconnect()
