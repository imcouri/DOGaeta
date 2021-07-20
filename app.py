
from flask import Flask
from flask import request
from nudenet import NudeClassifier
from nudenet import NudeDetector
from PIL import Image
import numpy as np
import urllib.request
import io

app = Flask(__name__)

@app.route('/')
def hello_world():
    URL = request.args.get('url')
    classifier = NudeClassifier()
    detector= NudeDetector()

    detectionsList = {}
    exposedDetections = {}
    coveredDetections = {}

    with urllib.request.urlopen(URL) as url:
        f = io.BytesIO(url.read())
    image = Image.open(f)
    result = classifier.classify(np.array(image))
    notSafeScore = result[0]['unsafe'] * 100
    safeScore = result[0]['safe'] * 100

    isSafe = result[0]['safe'] >= 50 and result[0]['unsafe'] < 60  # used later
    print(safeScore)
    print(notSafeScore)
    if notSafeScore > 70.0 and safeScore < 50.0:
        detect = detector.detect(np.array(image))
        for detection in detect:
            if detection['score'] * 100 >= 60:
                if 'EXPOSED' in detection['label']:
                    exposedDetections[detection['label']] = detection['score'] * 100
                elif 'COVERED' in detection['label']:
                    coveredDetections[detection['label']] = detection['score'] * 100
            else:
                return {
                    'safe': True,
                    'score': result[0],
                }
        if exposedDetections != None or coveredDetections != None:
            # for exposed in exposedDetections:
            #    if 'BREAST_F'
            detectionsList = {
                'exposed': exposedDetections,
                'covered': coveredDetections
            }
            return {
                'result': {
                    'safe': result[0]['safe'] * 100,
                    'unsafe': result[0]['unsafe'] * 100,
                },
                'detections': detectionsList,
                'safe': isSafe
            }
        else:
            return {
                'safe': True,
                'score': result[0],
            }

    return {
        'safe': True,
        'score': result[0],
    }


if __name__ == '__main__':
    app.run()