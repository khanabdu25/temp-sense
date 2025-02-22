import time
import board
import adafruit_dht
import paho.mqtt.client as mqtt
import json


dht_device = adafruit_dht.DHT11(board.D4)

# MQTT setup
MQTT_BROKER = "192.168.1.17"
MQTT_PORT = 1883
MQTT_TOPIC = "binary/updates"

def read_sensor():
    try:
        temperature_c = dht_device.temperature
        humidity = dht_device.humidity
        if temperature_c is not None and humidity is not None:
            temperature_f = temperature_c * 9 / 5 + 32
            return {"temperature_c": temperature_c, "temperature_f": temperature_f, "humidity": humidity}
        else:
            return None
    except Exception as e:
        print(f"Failed to retrieve data from humidity sensor: {e}")
        return None

def connect_mqtt():
    client = mqtt.Client()
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
            time.sleep(60)
    except KeyboardInterrupt:
        print("Stopped by User")
        dht_device.exit()
        client.disconnect()

if __name__ == "__main__":
    main()
