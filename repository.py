import socket
import pika
import sys
import time
import pymongo
import threading
import subprocess
import datetime

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
