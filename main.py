# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 21:02:03 2020

@author: My Laptop
"""

import DroneController
import time

def main():
    tello = DroneController.Tello()
    
    bat = tello.battery()
    
    if(bat>30):
        tello.takeoff()
        time.sleep(7)
        tello.land()
        tello.stop_connection()
    
if __name__ == '__main__':
    main()