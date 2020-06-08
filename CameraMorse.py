# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 23:11:22 2020

@author: Muhammad Fazlur Rahman
"""

import cv2 as cv

cap = cv.VideoCapture(0)

class CameraMorse:
    def __init__(self, dot_duration = 0.2, dash_duration = None, display = False, threshold = 20):
        
        self.dot_duration = dot_duration
        
        if (self.dash_duration is None):
            self.dash_duration = 3*self.dot_duration
        else:
            self.dash_duration = dash_duration
            
        self.threshold = threshold
        self.commands = {}
        
        self.is_pressed = False
        self.mean = 0
        
        self.timestamp = 0
        
        code = ""
        
        self.display = display
        if self.display:
            self.graph_brightness = RollingGraph(threshold=self.threshold)

    def define_command(self, code, command):
        self.command[code] = command
        
    def is_pressing(self, frame):
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        self.mean = cv.mean(gray)
        
        return self.mean < self.threshold
        
    def eval(self, frame):
        
        is_pressing = is_pressing(frame)
        current_time = time()
        
        detected = ""
        if (self.is_pressed and not is_pressing):
            duration = current_time - self.timestamp
            if duration <= self.dot_duration:
                self.code += "."
                detected = "dot"
            
            elif (duration > self.dot_duration and duration < self.dash_duration):
                self.code += "-"
                detected = "dash"
            
            else:
                self.code = ""
            
            self.is_pressed = False
            self.timestamp = current_time
            
        elif (not self.is_pressed and is_pressing):
            duration = current_time - self.timestamp
            if (duration > self.dash_duration):
                self.code = ""
            
            self.is_pressed = True
            self.timestamp = current_time
            
        return is_pressing, detected
                    
if __name__ == "__main__":
    print("Hello world!")
    
    
    #print(code)

    #cv.imshow('frame', frame)
    #if cv.waitKey(1) & 0xFF == ord('q'):
    #    break
    #cv.destroyAllWindows()
    #cap.release()
