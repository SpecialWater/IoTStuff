# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import time
import os
import sys
import threading
import datetime
import asyncio
import json
from azure.iot.device.aio import IoTHubModuleClient
from w1thermsensor import W1ThermSensor


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
        
        # connect the client.
        await module_client.connect()

        # Connect Sensor
        sensor = W1ThermSensor()
        print("Sensor active")
        data = {}
        data['temperature'] = 0
        tempOld = 0

        # define behavior for receiving an input message on input1
        while True:
            data['temperature'] = sensor.get_temperature() * 9 / 5 + 32
            json_body = json.dumps(data)
            temp = json.loads(json_body)

            if tempOld != temp['temperature']:
                print(temp['temperature'])
                print("forwarding message to output1 at {0}".format(datetime.datetime.now().time()))
                tempOld = temp['temperature']
                await module_client.send_message_to_output(json_body, "output1")

            # For testing by sending data to EndPoint
            # await module_client.send_message(json_body)

            time.sleep(.5)

    except Exception as e:
        print ( "Unexpected error %s " % e )
        raise

if __name__ == "__main__":
    asyncio.run(main())