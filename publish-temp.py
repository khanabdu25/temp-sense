import Adafruit_DHT
import paho.mqtt.client as mqtt
import json
import time

# Sensor setup
SENSOR = Adafruit_DHT.DHT22
PIN = 23  # Adjust if using a different GPIO pin

# MQTT setup
MQTT_BROKER = "192.168.1.17"
MQTT_PORT = 1883
MQTT_TOPIC = "binary/updates"

def read_sensor():
    humidity, temperature = Adafruit_DHT.read_retry(SENSOR, PIN)
    if humidity is not None and temperature is not None:
        # Optionally convert the temperature to Fahrenheit
        temperature_f = temperature * 9/5.0 + 32
        return {"temperature_c": temperature, "temperature_f": temperature_f, "humidity": humidity}
    else:
        print("Failed to retrieve data from humidity sensor")

def connect_mqtt():
    client = mqtt.Client("Pi_Temp_Humidity_Publisher")
    client.connect(MQTT_BROKER, port=MQTT_PORT)
    return client

def publish_sensor_data(client):
    sensor_data = read_sensor()
    if sensor_data:
        # Publishing as a JSON string
        client.publish(MQTT_TOPIC, json.dumps(sensor_data))
        print("Published data to topic {}: {}".format(MQTT_TOPIC, json.dumps(sensor_data)))

def main():
    client = connect_mqtt()
    try:
        while True:
            publish_sensor_data(client)
            time.sleep(60)  # Adjust publish frequency as necessary
    except KeyboardInterrupt:
        print("Stopped by User")
        client.disconnect()

if __name__ == "__main__":
    main()
