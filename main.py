from DroneController import Tello
from FaceDetection import detect_face
import time
import cv2 as cv

kpX = 0.11
kpY = 0.15
title = str("log/kpX= " + str(kpX) + ", kpY= " + str(kpY) + ".txt")

cap = cv.VideoCapture(0)

tello = Tello()

bat = tello.query_battery()

tello.takeoff()
tello.move_up(10)

start_time = time.time()

def set_limit(x: int, lower: int, upper: int):
    if x > upper:
        return upper
    elif x < lower:
        return lower
    else:
        return x
        
while True:
    time_pure = time.time() - start_time
    file1 = open(title,"a")
    
    frame = tello.get_frame_read().frame  # capturing frame from drone 
    
    diff_x, diff_y = detect_face(frame)
    
    cv.imshow("drone", frame)             
    
    controlX = diff_x * kpX
    controlY = diff_y * kpY
    
    controlX = set_limit(controlX, -35, 35)
    controlY = set_limit(controlY, -35, 35)
        
    tello.send_rc_control(int(controlX), 0, 0, 0)
    
    file1.write(str(time_pure) + ". " + str(diff_x) + "," + str(controlX) + "\n")
    file1.close()
    
    if cv.waitKey(1) & 0xFF == ord('q'):  # quit from script
        cap.release()
        cv.destroyAllWindows()
        tello.streamoff()
        tello.land()
        break