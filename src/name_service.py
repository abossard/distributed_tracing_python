from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Please call with /name"

# get name from url path
@app.route("/<name>")
def hello_name(name):
    return "!{}!".format(name)