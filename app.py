from flask import Flask
from nudenet import classifier
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello Sammy!'