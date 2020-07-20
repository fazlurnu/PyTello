# import the necessary packages
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template

from MyDrone import MyDrone

import threading
import argparse
import datetime
import imutils
import time
import cv2

app = Flask(__name__)

@app.route("/")
def home():
    myDrone = MyDrone()
    myDrone.print_here()
    return render_template("index.html")
    
@app.route("/about")
def about():
    return render_template("about.html")
    
if __name__ == "__main__":
    app.run(debug=True)