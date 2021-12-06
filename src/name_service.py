import os
from flask import Flask
from azure.storage.queue import (
        QueueClient,
        BinaryBase64EncodePolicy,
        BinaryBase64DecodePolicy
)

app = Flask(__name__)

storage_queue_connection = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
storate_queue_name = os.environ.get("STORAGE_QUEUE_NAME")

queue_client = QueueClient.from_connection_string(storage_queue_connection, queue_name=storate_queue_name)

try:
    queue_client.create_queue()
except:
    pass

@app.route("/")
def hello_world():
    return "Please call with /name or /process to process messages"

# get name from url path
@app.route("/<name>")
def hello_name(name):
    return "!{}!".format(name)

@app.route("/process")
def process_queue():
    messages = queue_client.receive_messages()
    contents = [message.content for message in messages]
    for message in messages:
        queue_client.delete_message(message.id, message.pop_receipt)
    return "Processed {} messages. (Content: {})".format(len(contents), contents)