import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
import traceback

import os
env = os.environ


def transmitSingleMQTTMsg(client, topic, payload):
    # print(username, password, payload.replace("'", '"'))
    try:
        client.publish(topic=topic, payload=payload.replace("'", '"'), qos=2)
        return True
    except Exception as err:
        print(err)
        traceback.print_exc()
        return False


def transmitSingleMQTTMsgWithoutClient(topic, payload):
    publish.single(topic=topic, payload=payload.replace("'", '"'), hostname=env.get('MQTT_HOST'), port=int(env.get(
        'MQTT_PORT')), client_id=env.get('MQTT_USER'), auth={'username': env.get('MQTT_USER'), 'password': env.get('MQTT_PASS'), }, qos=2, keepalive=3)
    # print("Send payload = [", payload, "] ok.")
    return 'success'


def subscribeSingleMQTTMsgWithoutClient(topic='iot/task_reponse', msg_count=1):
    if msg_count == 1:
        return subscribe.simple(topics=topic, qos=2, msg_count=msg_count, retained=False, hostname=env.get('MQTT_HOST'), port=int(env.get(
        'MQTT_PORT')), auth={'username': env.get('MQTT_USER'), 'password': env.get('MQTT_PASS'),}, keepalive=10).payload
    else:
        return [eval(str(i.payload, 'utf-8')) for i in subscribe.simple(topics=topic, qos=2, msg_count=msg_count, retained=False, hostname=env.get('MQTT_HOST'), port=int(env.get(
        'MQTT_PORT')), auth={'username': env.get('MQTT_USER'), 'password': env.get('MQTT_PASS'),}, keepalive=10)]