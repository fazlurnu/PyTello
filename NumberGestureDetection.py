# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 22:46:05 2020

@author: Fazlur
"""

# Imports
import numpy as np
import cv2 as cv
import math

cap = cv.VideoCapture(0)

face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
RED = (0, 0, 255)
BLACK = (0, 0, 0)

def detect_hand(frame, display=False):
    blur = cv.GaussianBlur(frame, (3,3), 0)
    hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)
    mask2 = cv.inRange(hsv, np.array([2,0,0]), np.array([20,255,255]))
    
    kernel = np.ones((5,5))
    dilation = cv.dilate(mask2, kernel, iterations = 1)
    erosion = cv.erode(dilation, kernel, iterations = 1) 
    filtered = cv.GaussianBlur(erosion, (3,3), 0)
    ret,thresh = cv.threshold(filtered, 127, 255, 0)
    cv.imshow("Thresholded", thresh)
    
def main():
    while True:
        ret, frame = cap.read()
        detect_hand(frame, display=True)
        
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        
if __name__ == "__main__":
    main()
    cap.release()
    cv.destroyAllWindows()