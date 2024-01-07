from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS from Flask-CORS
from flask_socketio import SocketIO

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()


app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


# InfluxDB Configuration
token = os.getenv("INFLUXDB_TOKEN")
org = "24-43"
url = "http://localhost:8086"
bucket = "smart_home_db"
influxdb_client = InfluxDBClient(url=url, token=token, org=org)


@socketio.on('connect')
def handle_connect():
    print('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


# Function to send alarm message to the client
def send_alarm_message_ws(topic, message):
    try:
        socketio.emit(topic, message)
    except Exception as e:
        print(e)

def send_alarm_clock_message_ws(topic, message):
    try:
        socketio.emit(topic, message)
    except Exception as e:
        print(e)


# MQTT Configuration
mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()


def on_connect(client, userdata, flags, rc):
    client.subscribe("Temperature")
    client.subscribe("Humidity")
    client.subscribe("Buttons")
    client.subscribe("Buzzers")
    client.subscribe("LED")
    client.subscribe("Keypads")
    client.subscribe("Pirs")
    client.subscribe("Distance")
    client.subscribe("Gyroscope")
    client.subscribe("LCD")
    client.subscribe("RGB")
    client.subscribe("IR")
    client.subscribe('alarm')
    client.subscribe('clock')


mqtt_client.on_connect = on_connect


def on_message_handler(client, userdata, msg):
    if msg.topic == 'alarm':
        send_alarm_message_ws('alarm_message', json.loads(msg.payload.decode('utf-8')))
    elif msg.topic == 'Buzzers':
        # TODO : Treba da salje i za budilnik da se ugasi
        send_alarm_message_ws('alarm_off_message', json.loads(msg.payload.decode('utf-8')))
        save_to_db(json.loads(msg.payload.decode('utf-8')))
    elif msg.topic == 'clock':
        send_alarm_message_ws('clock_message', json.loads(msg.payload.decode('utf-8')))
    else:
        save_to_db(json.loads(msg.payload.decode('utf-8')))


# Assign the on_message handler
mqtt_client.on_message = on_message_handler


def save_to_db(data):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    timestamp = datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else datetime.utcnow()
    point = (
        Point(data["measurement"])
        .tag("simulated", data["simulated"])
        .tag("runs_on", data["runs_on"])
        .tag("name", data["name"])
        .field("measurement", data["value"])
        .time(timestamp)
    )
    print(point)
    write_api.write(bucket=bucket, org=org, record=point)


@app.route('/')
def home():
    return f"Secret Key: {token}"


# Route to store dummy data
@app.route('/safety_system/<string:pin>', methods=['PUT'])
def safety_system(pin):
    try:
        print(pin, "set system PIN ============")
        try:
            mqtt_client.publish("safety_system",  pin)
        except Exception as e:
            print(e)
        # pin treba proslediti preko mqtt simulatoru
        return jsonify({"response": "Safety System set " + pin})
    except Exception as e:
        return jsonify({"response": "error - " + str(e)})


@app.route('/deactivate_alarm/<string:pin>', methods=['PUT'])
def deactivate_alarm(pin):
    try:
        print(pin, " deactivate PIN ============")
        try:
            mqtt_client.publish("deactivate_alarm",  pin)
        except Exception as e:
            print(e)
        # pin treba proslediti preko mqtt simulatoru
        return jsonify({"response": "Alarm deactivated " + pin})
    except Exception as e:
        return jsonify({"response": "error - " + str(e)})


@app.route('/set_alarm_clock/<string:time>', methods=['PUT'])
def alarm_clock(time):
    try:
        print(time, "set alarm clock ============")
        # format string-a: 2024-01-10T23:38
        try:
            mqtt_client.publish("alarm_clock",  time)
            print(time)
        except Exception as e:
            print(e)
        # pin treba proslediti preko mqtt simulatoru
        return jsonify({"response": "Alarm Clock set " + time})
    except Exception as e:
        return jsonify({"response": "error - " + str(e)})


@app.route('/deactivate_alarm_clock', methods=['GET'])
def deactivate_alarm_clock():
    try:
        try:
            mqtt_client.publish("turn_off_clock",  True)
        except Exception as e:
            print(e)
        # pin treba proslediti preko mqtt simulatoru
        return jsonify({"response": "Alarm clock turned off "})
    except Exception as e:
        return jsonify({"response": "error - " + str(e)})


#
# def handle_influx_query(query):
#     try:
#         query_api = influxdb_client.query_api()
#         tables = query_api.query(query, org=org)
#
#         container = []
#         for table in tables:
#             for record in table.records:
#                 container.append(record.values)
#
#         return jsonify({"status": "success", "data": container})
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)})
#
#
# @app.route('/simple_query', methods=['GET'])
# def retrieve_simple_data():
#     query = f"""from(bucket: "{bucket}")
#     |> range(start: -10m)
#     |> filter(fn: (r) => r._measurement == "Humidity")"""
#     return handle_influx_query(query)
#
#
# @app.route('/aggregate_query', methods=['GET'])
# def retrieve_aggregate_data():
#     query = f"""from(bucket: "{bucket}")
#     |> range(start: -10m)
#     |> filter(fn: (r) => r._measurement == "Humidity")
#     |> mean()"""
#     return handle_influx_query(query)


if __name__ == '__main__':
    app.run(debug=True, port=8085)
