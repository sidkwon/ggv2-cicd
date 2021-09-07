# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
import sys
import datetime
import time
import argparse

parser = argparse.ArgumentParser(description='Demo purposes')
parser.add_argument('--thing_name', type=str, action='store')
args, _ = parser.parse_known_args()

while True:
    
    # message = f"Hello, {sys.argv[1]}! Current time: {str(datetime.datetime.now())}."
    # message = 'AHA'
    # message = f"Hello, {sys.argv[1]}!"
    message = "Hello, {}".format(str(args.thing_name))
    
    # Print the message to stdout.
    print(message)
    
    # Append the message to the log file.
    with open('/tmp/Greengrass_HelloWorld.log', 'a') as f:
        print(message, file=f)
        
    time.sleep(1)

