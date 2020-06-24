# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 20:57:55 2020

@author: My Laptop
"""

class Tello(object):
    def __init__(self):
        print("init")
        
    def __del__(self):
        print("destroy")
        
def main():
    drone = Tello()
    print("Hello")
    
if __name__ == "__main__":
    main()