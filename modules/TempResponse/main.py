# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import time
import os
import sys
import asyncio
import json
from six.moves import input
import threading
from azure.iot.device import IoTHubModuleClient
import RPi.GPIO as GPIO

async def main():
    try:
        if not sys.version >= "3.5.3":
            raise Exception( "The sample requires python 3.5.3+. Current version of Python: %s" % sys.version )
        print ( "IoT Hub Client for Python" )

        # The client object is used to interact with your Azure IoT hub.
        module_client = IoTHubModuleClient.create_from_edge_environment()
        IoTHubModuleClient.create_from_edge_environment()
        #conn_str = "HostName=AndrewPiProject.azure-devices.net;DeviceId=RPi4;SharedAccessKey=FoUWxLuoWLZxKWN/ytg6qMCk0dWHSiWaysIart2CD/s="
        #module_client = IoTHubModuleClient.create_from_connection_string(conn_str)       

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.OUT, initial=GPIO.HIGH)
        time.sleep(1)
        GPIO.setup(21, GPIO.OUT, initial=GPIO.LOW)
        time.sleep(1)
        GPIO.setup(21, GPIO.OUT, initial=GPIO.HIGH)

        # connect the client.
        print("Trying to connect")
        module_client.connect()

        # define behavior for receiving an input message on input1
        input_message = 0
        while True:
            print('Receiving message')
            input_message = await module_client.receive_message_on_input("input1")  # blocking call
            message = json.loads(input_message)
            temperature = message['temperature']
            print("the data in the message received on input1 was ")
            print(temperature)
            if temperature > 79:
                print('HOT')
                GPIO.output(21, GPIO.HIGH)
            else:
                print('COLD')
                GPIO.output(21, GPIO.LOW)
            time.sleep(.5)

    except Exception as e:
        print ( "Unexpected error %s " % e )
        raise

if __name__ == "__main__":
    # If using Python 3.7 or above, you can use following code instead:
    asyncio.run(main())