from flask import jsonify, Flask, request, render_template, Response, url_for
from flask import make_response
from functools import wraps
import requests

app = Flask(__name__)
#!/usr/bin/env python3
import socket
import pika
import sys
import time
import pymongo
import threading
import subprocess
import datetime
import pdb

"""Imports for gpio"""
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
    GPIO.output(GPIO.LOW)

def redOn():
    blink(rPin)

def greenOn():
    blink(gPin)

def off():
    turnOff(rPin)
    turnOff(gPin)
    turnOff(bPin)
"""RPi GPIO LED end section"""

"""Flask Portion"""
def check_auth(username, password):
  #  return username == "admin" and password == "secret"

    userList = col.find_one({"user": username})
    passList = col.find_one({"Pass": password})
    return userList != None and passList != None

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
            "Could not verify your access level for that URL. \n"
            "You have to login with proper Hokie credentials",
            401,
            {"WWW_Authenticate": 'Basic realm="Login Required"'},
            )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated

    
templateData = {
        "title": "Hello!",
        "time": "",
        "4thFloor": "Empty",
        "2ndFloor": "Empty",
        "TorgBridge": "Empty",
        "color" : "green",
}

@app.route("/", methods=["GET"])
@requires_auth
def hello():
    if request.method == "GET":
        now = datetime.datetime.now()
        timeString = now.strftime("%Y-%m-%d %H:%M")
        templateData["time"] = timeString
        
        return render_template("main.html", **templateData)


@app.route("/4thLib", methods=['GET'])
@requires_auth
def return4thLib():
    if request.method == "GET":
        now = datetime.datetime.now()
        timeString = now.strftime("%Y-%m-%d %H:%M")
        templateData["time"] = timeString
        locString = "4th floor Lib"
        templateData["location"] = locString
        return render_template("main.html", **templateData)

@app.route("/2ndLib", methods=['GET'])
@requires_auth
def return2ndLib():
    if request.method == "GET":
        now = datetime.datetime.now()
        timeString = now.strftime("%Y-%m-%d %H:%M")
        templateData["time"] = timeString
        locString = "2nd floor Lib"
        templateData["location"] = locString
        return render_template("main.html", **templateData)

@app.route("/Torg", methods=['GET'])
@requires_auth
def returnTorg():
    if request.method == "GET":
        now = datetime.datetime.now()
        timeString = now.strftime("%Y-%m-%d %H:%M")
        templateData["time"] = timeString
        locString = "Torg Bridge"
        templateData["location"] = locString
        return render_template("main.html", **templateData)


def call4th(ch, method, properties, body):
    print("4th")

def call2nd(ch, method, properties, body):
    print("2nd")

def callTorg(ch, method, properties, body):
    print("Torg")


def startApp():

    channel.basic_consume(on_message_callback=call4th, queue='4Lib')
    channel.basic_consume(on_message_callback=call2nd, queue='2Lib')
    channel.basic_consume(on_message_callback=callTorg, queue='TorgB')
    
    channel.start_consuming()
    """ 
    while(1):
        x, y, returnMessage = channel.basic_get('4Lib')
        x, y, returnMessage = channel.basic_get('2Lib')
        x, y, returnMessage = channel.basic_get('TorgB')
    """

client = pymongo.MongoClient()
db = client.final_Proj
db.authenticate("Kishan", "Buse", source = "final_Proj")
col = db.service_Auth

if __name__ == "__main__":
#    app.run(host='0.0.0.0', port=80, debug=True)
    t = threading.Thread(target=startApp)
    t.start()

    user1 = {"user": "Kishan", "Pass": "Something", "Delete": "True"}
    user2 = {"user": "Buse", "Pass": "Honaker", "Delete": "True"}
    user3 = {"user": "Ethan", "Pass": "Password", "Delete": "True"}
    posts = [user1, user2, user3]
    col.insert_many(posts)


    """ 
    channel.basic_consume(on_message_callback=callback, queue='4Lib')
    channel.basic_consume(on_message_callback=callback, queue='2Lib')
    channel.basic_consume(on_message_callback=callback, queue='TorgB')

    channel.start_consuming()
    """
    app.run(host='0.0.0.0', port=80, debug=True)

