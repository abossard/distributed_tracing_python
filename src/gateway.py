from flask import Flask, request
import requests
import os

app = Flask(__name__)
nameService = os.environ.get('NAME_SERVICE') or "http://localhost:8081"

def call_name_service(name):
    return requests.get(nameService+"/"+name).text

@app.route("/")
def hello_world():
    return "Hello, World! You are " + call_name_service(request.user_agent.browser)