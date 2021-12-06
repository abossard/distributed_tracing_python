import os

import requests

from az_logging import wrap_the_app

from flask import Flask, request

app = Flask(__name__)

logger, tracer = wrap_the_app(__name__, app)

from azure.storage.queue import (
    QueueClient
)

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
    with tracer.span(name='calling services') as services_span:
        processing_result = trigger_message_processing()
        service_result = call_name_service(request.user_agent.browser)
    logger.info("Path: /")
    return "Hello, World! You are {}\n(Output: {})".format(
        service_result, processing_result
    )


logger.info("READY")
