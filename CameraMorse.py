import numpy as np
import cv2 as cv
from time import time, sleep

class CameraMorse:
    
    # Used to initialize drone take-off
    # Camera act as a button, when the camera is covered, button is pressed
    # The button is pressed (camera is covered) when the average value of the image is less than a threshold
    
    def __init__(self, dot_duration=0.2, dash_duration=None, blank_duration=None, display=False, threshold=40):
        
    