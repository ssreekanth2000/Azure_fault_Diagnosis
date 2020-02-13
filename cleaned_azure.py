#!/usr/bin/env python3

import random
import time
import serial
from azure.iot.device import IoTHubDeviceClient, Message

# The device connection string to authenticate the device with your IoT hub.
CONNECTION_STRING = "HostName=Watts-Paid.azure-devices.net;DeviceId=FinalP1;SharedAccessKey=nR/asSSTfPg/Zgkr+JugFhGhrEexNiwisaf358YwmgE="

# Message structure is defined here
MSG_TXT = '{{"temperature":{temperature},"device":{device},"timestamp1":{timestamp1},"timestamp2":{timestamp2},"battery":{battery}}}'

ser = serial.Serial("/dev/ttyUSB0", 9600)
timestamp4 = time.time()


def iothub_client_init():
    # Create an IoT Hub client using the deivce connection string
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client


def iothub_client_telemetry_sample_run():
    try:
        client = iothub_client_init()
        print("IoT Hub device sending periodic messages, press Ctrl-C to exit")

        while True:
            while ser.in_waiting > 0:  # While there is data in Serial
                line = ser.readline()  # Read a line in serial
                # print("Line: {}".format(line))
                try:
                    line1 = str(line.decode("UTF-8"))
                except:
                    msg_txt_formatted = MSG_TXT.format(
                        temperature="err",
                        device="err",
                        timestamp1="decode err",
                        timestamp2="err",
                        battery="err",
                    )
                    message = Message(msg_txt_formatted)
                    print("Sending message: {}".format(message))
                    client.send_message(message)
                broken_line = line1.replace("\r", "").replace("\n", "").split(",")
                # print("Broken line: {}".format(broken_line))
                # Extract vlues from the serial line
                try:
                    device = broken_line[0]
                    battery = broken_line[1]
                    timestamp2 = time.time()
                except:
                    device = 00
                    battery = 00
                    timestamp2 = time.time()


                # print (broken_line)
                t0 = 2
                while t0 < (len(broken_line) - 1):

                    temperature = broken_line[t0 + 1]
                    timestamp1 = broken_line[t0]
                    # print(t0)
                    t0 = t0 + 2
                    msg_txt_formatted = MSG_TXT.format(
                        temperature=temperature,
                        device=device,
                        timestamp1=timestamp1,
                        timestamp2=timestamp2,
                        battery=battery,
                    )
                    message = Message(msg_txt_formatted)
                    print("Sending message: {}".format(message))
                    client.send_message(message)

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("IoTHubClient sample stopped")


if __name__ == "__main__":
    print("IoT Hub Quickstart #1 - Simulated device")
    print("Press Ctrl-C to exit")
    print("Configuring XBee...")

    ser.write("+".encode("ascii"))
    time.sleep(0.1)
    ser.write("+".encode("ascii"))
    time.sleep(0.1)
    ser.write("+".encode("ascii"))

    while ser.in_waiting < 2:
        pass

    print(ser.read(ser.in_waiting))

    time.sleep(1)
    ser.write("ATSM8\r".encode("ascii"))  # Synchronized sleep
    time.sleep(1)
    ser.write("ATSO1\r".encode("ascii"))  # SLeep coordinator
    time.sleep(1)
    # TODO: Some of these comments are wrong!
    ser.write("ATSPEA60\r".encode("ascii"))  # Be awake for 0.5 sec
    # ser.write("ATSP3E8\r".encode("ascii")) # Be awake for 1 sec (doesn't work?)
    time.sleep(1)
    ser.write("ATST1F4\r".encode("ascii"))  # Be asleep for 10min
    # ser.write("ATST3E8\r".encode("ascii")) # Be asleep for 10sec
    time.sleep(4)

    print("XBee configured.  Starting server...")

    iothub_client_telemetry_sample_run()
