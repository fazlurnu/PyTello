import DroneController
import time
import cv2 as cv

def main():
    tello = DroneController.Tello()
    
    bat = int(tello.battery())
    
    if (bat>30):
        tello.takeoff()
        time.sleep(8)        
        
        angle = 0
        for i in range(12):
            print(angle)
            tello.rotate_cw(30)
            angle+=30
        
        time.sleep(3)
        
        tello.land()
        tello.stop_connection()
    
if __name__ == '__main__':
    main()