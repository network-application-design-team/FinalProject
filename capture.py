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
channel.exchange_declare(exchange="Places", exchange_type="direct")





# Requires infinite while loop, may require multi-threading
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)

prevState = 2
cap = "Empty";
try:
    while True:
       # print(node)
        # Take the reading
        input = GPIO.input(4)
        # Test if input is high or low
        if (input != prevState): 
            time.sleep(5)
            if (input == 1):
                cap = "Full"
            else:
                cap = "Empty"
            if place == "4thLib":
                channel.basic_publish(
                exchange='Places', routing_key='4Lib', body=cap
                )
            elif place == "2ndLib":
                channel.basic_publish(
                exchange='Places', routing_key='2Lib', body=cap
                )


            elif place == "Torg":
                channel.basic_publish(
                exchange='Places', routing_key='TorgB', body=cap
                )
            else:
                print("Not a correct place")
            prevState = input
        # Slight Pause
        time.sleep(.1)
except KeyboardInterrupt:
    pass
finally:
        
        GPIO.cleanup()

