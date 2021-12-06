import os

import requests
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace import config_integration
from opencensus.trace.samplers import AlwaysOnSampler
from opencensus.trace.tracer import Tracer

config_integration.trace_integrations(['logging'])
logging.basicConfig(format='%(asctime)s traceId=%(traceId)s spanId=%(spanId)s %(message)s')
tracer = Tracer(sampler=AlwaysOnSampler())

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler())

from azure.storage.queue import (
    QueueClient
)
from flask import Flask, request

app = Flask(__name__)

middleware = FlaskMiddleware(
    app,
    exporter=AzureExporter()
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
    with tracer.span(name='hello'):
        logger.warning('In the span')
    logger.info("Path: /")
    return "Hello, World! You are {}\n(Output: {})".format(
        call_name_service(request.user_agent.browser),
        trigger_message_processing()
    )
