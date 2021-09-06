import time
import traceback
import json

import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.client as client
from awsiot.greengrasscoreipc.model import (
    IoTCoreMessage,
    QOS,
    SubscribeToIoTCoreRequest
)

import argparse

parser = argparse.ArgumentParser(description='Demo purposes')
parser.add_argument('--thing_name', type=str, action='store')
args, _ = parser.parse_known_args()

thing_name = args.thing_name

TIMEOUT = 10

ipc_client = awsiot.greengrasscoreipc.connect()

class StreamHandler(client.SubscribeToIoTCoreStreamHandler):
    def __init__(self):
        super().__init__()

    def on_stream_event(self, event: IoTCoreMessage) -> None:
        try:
            message = str(event.message.payload, "utf-8") # bytes to str
            topic_name = event.message.topic_name
            # Handle message.
            with open('/tmp/Greengrass_Subscriber.log', 'a') as f:
                message_dict = json.loads(message) # str to dict
                print('message_dict: {}'.format(message_dict), file=f)
                print('body: {}'.format(message_dict['body']), file=f)
                print('now: {}'.format(message_dict['now']), file=f)
                print('thing_name: {}'.format(message_dict['thing_name']), file=f)
                # print(event, file=f)
                # print(event.message.payload['body'], file=f)
                # print(message, file=f)
                # print('event.message.payload type: {}'.format(type(event.message.payload)), file=f)
                
            # print('event: {}'.format(event))
            # print('event.message.payload type: {}'.format(type(event.message.payload)))
            
        except:
            traceback.print_exc()

    def on_stream_error(self, error: Exception) -> bool:
        # Handle error.
        return True  # Return True to close stream, False to keep stream open.

    def on_stream_closed(self) -> None:
        # Handle close.
        pass


# topic = "my/topic"
topic = "sinjoonk/{}/topic".format(thing_name)

qos = QOS.AT_MOST_ONCE

request = SubscribeToIoTCoreRequest()
request.topic_name = topic
request.qos = qos
handler = StreamHandler()
operation = ipc_client.new_subscribe_to_iot_core(handler)
future = operation.activate(request)
future.result(TIMEOUT)

# Keep the main thread alive, or the process will exit.
while True:
    time.sleep(10)
                  
# To stop subscribing, close the operation stream.
operation.close()