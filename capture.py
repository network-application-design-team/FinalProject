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
    
credentials = pika.PlainCredentials(username, password)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(node, 5672, "/", credentials)
)
channel = connection.channel()
channel.exchange_declare(exchange="Place", exchange_type="direct")


# Requires infinite while loop, may require multi-threading
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN)

prev_input = 0
try:
    while True:
        # Take the reading
        input = GPIO.input(4)
        # If last reading was low and this is high, alert
        if ((not prev_input) and input):
            print("Under Pressure")
            print(input)
        # Update prev_input
        prev_input = input
        # Slight Pause
        time.sleep(0.1)
except KeyboardInterrupt:
    passfinally:
        GPIO.cleanup()

