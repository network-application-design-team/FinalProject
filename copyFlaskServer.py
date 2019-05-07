from six.moves import input
#from zeroconf import ServiceBrowser, Zeroconf, ServiceInfo
from flask import make_response, Flask, request, render_template, Response, url_for


from functools import wraps
import datetime
import socket
import time
import pymongo
import sys
#import time

import threading
import subprocess
import datetime
import pdb
import pika

app = Flask(__name__)
#!/usr/bin/env python3

"""imports for Canvas API"""
#import urllib as ul
#from urllib.error import HTTPError as hpe

"""General imports used for multiple sections"""
import json
import os, sys, time
import requests

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

channel.queue_declare(queue='4Lib')

channel.queue_bind(exchange='Places', queue='4Lib', routing_key='4Lib')
channel.queue_declare(queue='2Lib')
channel.queue_bind(exchange='Places', queue='2Lib', routing_key='2Lib')
channel.queue_declare(queue='TorgB')
channel.queue_bind(exchange='Places', queue='TorgB',  routing_key='TorgB')

def callback(ch, method, properties, body):
    checkpoint = 1
    print(" hot")
    

"""
def basic_consume(self,
                  queue,
                  on_message_callback,
                  auto_ack=False,
                  exclusive=False,
                  consumer_tag=None,
                  arguments=None):
    print("hot")
"""
#channel.basic_consume(callback, queue='4thLib', no_ack=True)
#channel.basic_consume(callback, queue='2ndLib', no_ack=True)

"""RPi GPIO LED section"""
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
    GPIO.output(pin, GPIO.LOW)

def redOn():
    blink(rPin)

def greenOn():
    blink(gPin)

def redOff():
    turnOff(rPin)

def greenOff():
    turnOff(gPin)

def whiteOff():
    turnOff(rPin)
    turnOff(gPin)
    turnOff(bPin)
"""RPi GPIO LED end section"""


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """

    userList = col.find_one({"user": username})
    passList = col.find_one({"Pass": password})
    # return username == "admin" and password == "secret"
    return userList != None and passList != None


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        "Could not verify your access level for that URL.\n"
        "You have to login with proper credentials",
        401,
        {"WWW-Authenticate": 'Basic realm="Login Required"'},
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated

FourthVal = "Empty"
SecondVal = "Empty"
TorgVal = "Empty"


templateData = {
        "title": "Hello!",
        "time": "",
        "FourthFloor": FourthVal,
        "SecondFloor": SecondVal,
        "TorgBridge": TorgVal
}



@app.route("/", methods=["GET"])
@requires_auth
def hello():
    if request.method == "GET":
        global FourthVal
        global SecondVal
        global TorgVal
        now = datetime.datetime.now()
        timeString = now.strftime("%Y-%m-%d %H:%M")
        templateData["time"] = timeString
        print(templateData)
        return render_template("main.html", time=timeString, FourthFloor=templateData["FourthFloor"], SecondFloor=templateData["SecondFloor"], TorgBridge=templateData["TorgBridge"])

@app.route("/4thLib", methods=['GET'])
@requires_auth
def return4thLib():
    if request.method == "GET":
        now = datetime.datetime.now()
        timeString = now.strftime("%Y-%m-%d %H:%M")
        templateData["time"] = timeString
        

        return render_template("main.html", **templateData)

@app.route("/2ndLib", methods=['GET'])
@requires_auth
def return2ndLib():
    if request.method == "GET":
        now = datetime.datetime.now()
        timeString = now.strftime("%Y-%m-%d %H:%M")
        templateData["time"] = timeString
        

        return render_template("main.html", **templateData)

@app.route("/Torg", methods=['GET'])
@requires_auth
def returnTorg():
    if request.method == "GET":
        now = datetime.datetime.now()
        timeString = now.strftime("%Y-%m-%d %H:%M")
        templateData["time"] = timeString
        

        return render_template("main.html", **templateData)

@app.route("/Update/<location>/<cap>")
def changeLoc(location, cap):
    if location  == "Torg":
        templateData["TorgBridge"] = cap
    elif location == "Fourth":
        templateData["FourthFloor"] = cap
    elif location == "Second":
        templateData["SecondFloor"] = cap
    return "0"


def call4th(ch, method, properties, body):
    x, y, place = channel.basic_get('4Lib')
    p = body.decode('utf-8')
    if p == "Full":
        greenOff()
        redOn()
        FourthVal = "Full"
        send = "http://" + str(ip) + "/Update/Fourth/Full"
        r = requests.get(send)
      #  print("4thLib is Full")
    if p == "Empty":
        redOff()
        greenOn()
        send = "http://" + str(ip) + "/Update/Fourth/Empty"
        r = requests.get(send)

def call2nd(ch, method, properties, body):
    x, y, place = channel.basic_get('2Lib')
    
    p = body.decode('utf-8')
    if p == "Full":
        greenOff()
        redOn()
        send = "http://" + str(ip) + "/Update/Second/Full"
        r = requests.get(send)
        SecondVal = "Full"
       # print("2ndLib is Full")
    if p == "Empty":
        redOff()
        greenOn()
        send = "http://" + str(ip) + "/Update/Second/Empty"
        r = requests.get(send)


def callTorg(ch, method, properties, body):
    
    #x, y, place = channel.basic_get('TorgB')
    #channel.basic_consume(queue
    p = body.decode('utf-8')
#    print(p)
    if p == "Full":
        greenOff()
        redOn()
        send = "http://" + str(ip) + "/Update/Torg/Full"
        
        r = requests.get(send)
    if p == "Empty":
        redOff()
        greenOn()
        send = "http://" + str(ip) + "/Update/Torg/Empty"
        r = requests.get(send)
    

def startApp():
    channel.basic_consume(on_message_callback=call4th, queue='4Lib',auto_ack=True)
    channel.basic_consume(on_message_callback=call2nd, queue='2Lib',auto_ack=True)
    channel.basic_consume(on_message_callback=callTorg, queue='TorgB', auto_ack=True)
    #print("yes")
    channel.start_consuming()


"""Pymongo"""
client = pymongo.MongoClient()
db = client.final_Proj
db.authenticate("Kishan", "Buse", source="final_Proj")
col = db.service_auth

if __name__ == "__main__":
    try:
        t = threading.Thread(target=startApp)
        t.start()
        FourthVal = "Empty"
        SecondVal = "Empty"
        TorgVal = "Empty"
        user1 = {"user": "Kishan", "Pass": "Something", "Delete": "True"}
        user2 = {"user": "Buse", "Pass": "Honaker", "Delete": "True"}
        user3 = {"user": "Ethan", "Pass": "Password", "Delete": "True"}
        posts = [user1, user2, user3]
        col.insert_many(posts)
        app.run(host="0.0.0.0", port=80, debug=True)
    except KeyboardInterrupt:
#        zeroconf.close()
        channel.queue_delete(queue='TorgB')
        channel.queue_delete(queue='2Lib')
        channel.queue_delete(queue='4Lib')
        connection.close()
        col.delete_many({"Delete": "True"})
        whiteOff()
        redOff()
        greenOff()
        GPIO.cleanup()
       
       
