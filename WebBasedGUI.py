# import the necessary packages
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
from DroneController import Tello

app = Flask(__name__)

is_flying = False

@app.route("/")
def home():
    return render_template("index.html")
    
@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/TO_LD')
def TO_LD():
    global is_flying
    
    if (is_flying):
        print("Landing")
        
    else:
        print("Take off")

    is_flying = not(is_flying)

    #print ("Drone is flying: " + str(is_flying))
    return ("nothing")

@app.route('/connect')
def connect():
    print("connect")
    return ("nothing")
    
if __name__ == "__main__":
    app.run(debug=True)