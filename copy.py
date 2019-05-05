from six.moves import input
#from zeroconf import ServiceBrowser, Zeroconf, ServiceInfo
from flask import Flask, request, render_template, Response, url_for

from functools import wraps
import datetime
import socket
import time
import pymongo

app = Flask(__name__)
#!/usr/bin/env python3

"""imports for Canvas API"""
import urllib as ul
from urllib.error import HTTPError as hpe

"""General imports used for multiple sections"""
import json
import os, sys, time
import requests

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


@app.route("/", methods=["GET"])
@requires_auth
def hello():
    if request.method == "GET":
        now = datetime.datetime.now()
        timeString = now.strftime("%Y-%m-%d %H:%M")
        templateData["time"] = timeString

        return render_template("main.html", **templateData)

"""Pymongo"""
client = pymongo.MongoClient()
db = client.ECE4564_Assignment_3
db.authenticate("Kishan", "Buse", source="ECE4564_Assignment_3")
col = db.service_auth

if __name__ == "__main__":
    try:
        user1 = {"user": "Kishan", "Pass": "Something", "Delete": "True"}
        user2 = {"user": "Buse", "Pass": "Honaker", "Delete": "True"}
        user3 = {"user": "Ethan", "Pass": "Password", "Delete": "True"}
        posts = [user1, user2, user3]
        col.insert_many(posts)
        app.run(host="0.0.0.0", port=80, debug=True)
    except KeyboardInterrupt:
#        zeroconf.close()
        col.delete_many({"Delete": "True"})
