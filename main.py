from DroneController import Tello
import time
import cv2 as cv

def main():
    tello = Tello()
    
    tello.connect()
    
    tello.takeoff()
    time.sleep(8)
    tello.land()
    
if __name__ == '__main__':
    main()