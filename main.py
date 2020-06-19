# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 21:02:03 2020

@author: My Laptop
"""

import DroneController
import time

def main():
    tello = DroneController.Tello()
    
    prev_time = time.time()
    interval = 5
    time.sleep(2)
    tello.takeoff()
    
    while True:
        curr_time = time.time()
        if(curr_time - prev_time > interval):
            prev_time = curr_time
            tello.land()
            break
    
if __name__ == '__main__':
    main()