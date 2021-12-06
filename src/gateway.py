import os

import requests
from azure.storage.queue import (
    QueueClient
)
from flask import Flask, request

app = Flask(__name__)
name_service_url = os.environ.get('NAME_SERVICE') or "http://localhost:8081"
storage_queue_connection = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
storage_queue_name = os.environ.get("STORAGE_QUEUE_NAME")
queue_client = QueueClient.from_connection_string(storage_queue_connection, queue_name=storage_queue_name)


def call_name_service(name):
    queue_client.send_message(name)
    return requests.get(name_service_url + "/" + name).text


def trigger_message_processing():
    return requests.get(name_service_url + "/process").text


@app.route("/")
def hello_world():
    return "Hello, World! You are {}\n(Output: {})".format(
        call_name_service(request.user_agent.browser),
        trigger_message_processing()
    )
