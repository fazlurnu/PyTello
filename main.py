from DroneController import Tello
from FaceDetection import detect_face
import time
import cv2 as cv

cap = cv.VideoCapture(0)

tello = Tello()

bat = tello.query_battery()

tello.takeoff()
tello.move_up(10)

while True:
    frame = tello.get_frame_read().frame  # capturing frame from drone 
    
    diff_x, diff_y = detect_face(frame)
    
    cv.imshow("drone", frame)             
    
    tello.send_rc_control(int(diff_x/4), 0, int(-diff_y/4), 0)
    
    if cv.waitKey(1) & 0xFF == ord('q'):  # quit from script
        cap.release()
        cv.destroyAllWindows()
        tello.land()
        break