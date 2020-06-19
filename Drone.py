# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 05:10:03 2020

@author: My Laptop
"""

class Drone:
    def __init__(self):
        print("Create object")
        
    def __del__(self):
        print("Destroy object")
        
def main():
    print("Initialize")
    drone = Drone()
    print("End program")
    
    
if __name__ == "__main__":
    main()