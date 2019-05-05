#!/usr/bin/env python3
import socket
import pika
import sys
import time
import pymongo
import threading
import subprocess
import datetime

# imports for pressure sensor
import RPi.GPIO as GPIO

username = "Honaker"
password = "buse"

node = sys.argv[2]
place = sys.argv[4]
    
credentials = pika.PlainCredentials(username, password)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(node, 5672, "/", credentials)
)
channel = connection.channel()
channel.exchange_declare(exchange="Place", exchange_type="direct")





# Requires infinite while loop, may require multi-threading
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)

try:
    while True:
        # Take the reading
        input = GPIO.input(4)
        # Test if input is high or low
        if (input == 1):
            if place == "4thLib":
                
                channel.basic_publish(
                exchange=location, routing_key='4Lib', body=place
            )

            elif place == "2ndLib":

                channel.basic_publish(
                exchange=location, routing_key='2Lib', body=place
            )


            elif place == "Torg":
                channel.basic_publish(
                exchange=location, routing_key='TorgB', body=place
            )


            else:
                print("Not a correct place")
        # Slight Pause
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
        
        GPIO.cleanup()

