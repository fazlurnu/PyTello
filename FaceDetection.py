import cv2 as cv
from Matrix import matrix
from KalmanFilter import kalman_filter

from time import time
import numpy as np

cap = cv.VideoCapture(0)

face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
RED = (0, 0, 255)
BLACK = (0, 0, 0)
    
def detect_face(frame, display = False):
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    frame_height = frame.shape[0]
    frame_width = frame.shape[1]
    
    center = (int(frame_width/2), int(frame_height/2))
    #print(frame_widht, frame_height)
    
    cv.circle(frame, center, 5, RED, 2)
    
    if (len(faces) > 0):
        is_deteceted = True
    else:
        is_deteceted = False
        
    if is_deteceted:
        for i, (x, y, w, h) in enumerate(faces):
            center_face = (int(x + w/2), int(y + h/2))
    
    else:
        center_face = (0,0)
        (x,y,w,h) = (0,0,0,0)
        is_deteceted = False
        
    return center_face, (x,y,w,h), is_deteceted
    
def main():
    
    states = matrix([[0.],
                     [0.],
                     [0.],
                     [0.]])
    
    xhat = int(states.value[0][0])
    yhat = int(states.value[2][0])
    
    P = matrix([[1000., 0., 0., 0.],
                [0., 1000., 0., 0.],
                [0., 0., 1000., 0.],
                [0., 0., 0., 1000.]]) # initial uncertainty

    ret, frame = cap.read()
    
    display = True
    time_prev = time()
    
    while True:
        ret, frame_now = cap.read()
        
        # operation
        center_face_now, (x,y,w,h), is_detected_now = detect_face(frame_now)
        dt = time() - time_prev
    
        if(is_detected_now):
            time_prev = time()            
            
            z = matrix([[x],[y]])
            states, P = kalman_filter(states, P, z, dt)
            xhat = int(states.value[0][0])
            yhat = int(states.value[2][0])
            what = w
            hhat = h
            
            cv.rectangle(frame_now, (xhat, yhat), (xhat+w, yhat+h), RED, 2)
            cv.rectangle(frame_now, (x, y), (x+w, y+h), BLUE, 2)
        
        else:
            states, P = kalman_filter(states, P, z, dt, data_ok=False)
            xhat = int(states.value[0][0])
            yhat = int(states.value[2][0])
            
            cv.rectangle(frame_now, (xhat, yhat), (xhat+what, yhat+hhat), RED, 2)
                
        if(display):
            print(dt)
            cv.imshow('frame', frame_now)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
                

if __name__ == "__main__":
    main()
    cap.release()
    cv.destroyAllWindows()
    
