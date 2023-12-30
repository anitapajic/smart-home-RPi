import json
import time
import paho.mqtt.client as mqtt
mqtt_broker_address = "localhost"
mqtt_broker_port = 1883

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("safety_system")


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode("utf-8"))
        home = userdata['home']
        time.sleep(10)
        home.set_pin(str(data) + "#")
        print(f"Safety system set: {home.safety_system}")
        print(f"Pin: {home.alarm_pin}")

        # Process the received data as needed
    except json.JSONDecodeError as e:
        print(f"Error decoding MQTT message: {str(e)}")
def listen_for_mqtt(mqtt, on_connect, on_message, home):
    # Set up the MQTT client
    try:
        mqtt_client_simulator = mqtt.Client(userdata={'home':home})
        mqtt_client_simulator.on_connect = on_connect
        mqtt_client_simulator.on_message = on_message

        # Connect to the MQTT broker
        mqtt_client_simulator.connect(mqtt_broker_address, mqtt_broker_port, 60)
        mqtt_client_simulator.loop_start()
    except Exception as e:
        print(e)