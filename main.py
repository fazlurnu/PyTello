# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 21:02:03 2020

@author: My Laptop
"""

import DroneController
import time

def main():
    tello = DroneController.Tello()
    
    response = tello.takeoff()
    
    print(response)
    time.sleep(10)
    
    response = tello.land()
    
    #if (response == 'ok'):
    #    tello.stop_connection()
    
if __name__ == '__main__':
    main()