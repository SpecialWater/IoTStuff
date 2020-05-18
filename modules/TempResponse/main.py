# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import time
import os
import sys
import asyncio
from six.moves import input
import threading
from azure.iot.device import IoTHubModuleClient
import RPi.GPIO as GPIO

def main():
    try:
        if not sys.version >= "3.5.3":
            raise Exception( "The sample requires python 3.5.3+. Current version of Python: %s" % sys.version )
        print ( "IoT Hub Client for Python" )

        # The client object is used to interact with your Azure IoT hub.
        module_client = IoTHubModuleClient.create_from_edge_environment()
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
            input_message = module_client.receive_message_on_input("input1")  # blocking call
            print("the data in the message received on input1 was ")
            print(input_message.data)
            print("Blink LED if hot")
            if int(input_message.data) > 79:
                print('HOT')
                GPIO.output(21, GPIO.HIGH)
            else:
                print('COLD')
                GPIO.output(21, GPIO.LOW)

    except Exception as e:
        print ( "Unexpected error %s " % e )
        raise

if __name__ == "__main__":
    # If using Python 3.7 or above, you can use following code instead:
    main()