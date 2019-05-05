import socket
import pika
import sys
import time
import pymongo
import threading
import subprocess
import datetime

# Imports for gpio
import RPi.GPIO as GPIO

def fetch_ip():
    return((([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close())\
      for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0])


ip = fetch_ip()


username = "Honaker"
password = "buse"

credentials = pika.PlainCredentials(username, password)

connection = pika.BlockingConnection(pika.ConnectionParameters(ip, 5672, '/', credentials))
channel = connection.channel()

channel.exchange_declare(exchange='Places', exchange_type='direct')

channel.queue_declare(queue='4thLib')
channel.queue_bind(exchange='Places', queue='4thLib', routing_key='4thLib')
channel.queue_declare(queue='2ndLib')
channel.queue_bind(exchange='Places', queue='2ndLib', routing_key='2ndLib')
channel.queue_declare(queue='Torg')
channel.queue_bind(exchange='Places', queue='Torg',  routing_key='Torg')

def callback(ch, method, properties, body):
    checkpoint = 1
    print(" hot")
   

channel.basic_consume(callback, queue='4thLib', no_ack=True)
channel.basic_consume(callback, queue='2ndLib', no_ack=True)
channel.basic_consume(callback, queue='Torg', no_ack=True)

channel.start_consuming()

# RPi GPIO section 
rPin = 11
gPin = 13
bPin = 15

GPIO.setwarnings(False)

def blink(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

def turnOff(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(GPIO.LOW)

def redOn():
    blink(rPin)

def greenOn():
    blink(gPin)

def off():
    turnOff(rPin)
    turnOff(gPin)
    turnOff(bPin)

    


