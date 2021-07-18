from flask import Flask
from nudenet import NudeClassifier
app = Flask(__name__)

@app.route('/')
def hello_world():
    classifier = NudeClassifier()
    return 'Hello Sammy!'