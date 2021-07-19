
from flask import Flask
from flask import request
from nudenet import NudeClassifier
from PIL import Image
import numpy as np
import urllib.request
import io

app = Flask(__name__)

@app.route('/')
def hello_world():
    URL = request.args.get('url')
    classifier = NudeClassifier()
    with urllib.request.urlopen(URL) as url:
        f = io.BytesIO(url.read())
    image = Image.open(f)
    result = classifier.classify(np.array(image))
    return result


if __name__ == '__main__':
    app.run(debug=True)