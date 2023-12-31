import json
import time
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME, PORT


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("safety_system")
    client.subscribe("deactivate_alarm")


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode("utf-8"))
        home = userdata['home']
        alarm = userdata['alarm']
        if msg.topic == 'safety_system':
            time.sleep(10)
            home.set_pin(str(data) + "#")
            print(f"Safety system set: {home.safety_system}")
            print(f"Pin: {home.alarm_pin}")
        elif msg.topic == 'deactivate_alarm':
            if home.alarm_pin == str(data) + "#":
                home.safety_system = False
                home.alarm = False
                alarm.clear()
                print(f"Alarm deactivated")
            else:
                print(f"Wrong pin")

        # Process the received data as needed
    except json.JSONDecodeError as e:
        print(f"Error decoding MQTT message: {str(e)}")
def listen_for_mqtt(mqtt, on_connect, on_message, home, alarm):
    # Set up the MQTT client
    try:
        mqtt_client_simulator = mqtt.Client(userdata={'home':home, 'alarm': alarm})
        mqtt_client_simulator.on_connect = on_connect
        mqtt_client_simulator.on_message = on_message

        # Connect to the MQTT broker
        mqtt_client_simulator.connect(HOSTNAME, PORT, 60)
        mqtt_client_simulator.loop_start()
    except Exception as e:
        print(e)