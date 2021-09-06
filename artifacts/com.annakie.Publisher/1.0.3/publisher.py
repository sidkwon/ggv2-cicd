import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.client as client
from awsiot.greengrasscoreipc.model import (
    QOS,
    PublishToIoTCoreRequest
)
import time
import json
import argparse

parser = argparse.ArgumentParser(description='Demo purposes')
parser.add_argument('--thing_name', type=str, action='store')
args, _ = parser.parse_known_args()

thing_name = args.thing_name

TIMEOUT = 10

ipc_client = awsiot.greengrasscoreipc.connect()
                    
topic = "sinjoonk/{}/topic".format(thing_name)
# topic = "sinjoonk/sinjoonk-ggv2-core/topic"
print('=====================================================')
print("topic: {}".format(topic))

qos = QOS.AT_LEAST_ONCE

while True:
    # Create a message
    message = {}
    message['body'] = "Hello, World"
    message['now']  = time.strftime('%y-%m-%d %H:%M:%S')
    message['thing_name'] = args.thing_name
    message['component_version'] = '1.0.3'

    request = PublishToIoTCoreRequest()
    request.topic_name = topic
    request.payload = bytes(json.dumps(message), "utf-8")
    request.qos = qos
    operation = ipc_client.new_publish_to_iot_core()
    operation.activate(request)
    future = operation.get_response()
    future.result(TIMEOUT)
    
    time.sleep(10)