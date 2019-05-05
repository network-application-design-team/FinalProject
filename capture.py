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
connection = pika.BlockingConnection(
    pika.ConnectionParameters(node, 5672, "/", credentials)
)
channel = connection.channel()
channel.exchange_declare(exchange="Place", exchange_type="direct")

connection.close()
