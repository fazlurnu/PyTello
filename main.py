# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 21:02:03 2020

@author: My Laptop
"""

import DroneController
import time

def main():
    tello = DroneController.Tello()
    
    tello.takeoff()
    time.sleep(1)
    tello.land()
    
if __name__ == '__main__':
    main()