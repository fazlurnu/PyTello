import DroneController
import time
import cv2 as cv

def main():
    tello = DroneController.Tello()
    
    bat = int(tello.battery())
    
    if (bat>30):
        tello.takeoff()
        time.sleep(7)        
        
        tello.rotate_cw(30)
        time.sleep(7)
        tello.rotate_ccw(30)
        time.sleep(7)
        
        tello.land()
        tello.stop_connection()
    
if __name__ == '__main__':
    main()