# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 21:02:03 2020

@author: My Laptop
"""

import DroneController
import time

prev_time = time.time()

def main():
    tello = DroneController.Tello()
    
    curr_time = time.time()
    interval = 10
    tello.takeoff()
    
    if(curr_time - prev_time > interval):
        prev_time = curr_time
        tello.land()
    
if __name__ == '__main__':
    main()