from DroneController import Tello
from FaceDetection import detect_face
import time
import cv2 as cv

cap = cv.VideoCapture(0)

tello = Tello()
tello.connect()

bat = tello.query_battery()

tello.streamon()

tello.takeoff()
tello.move_up(20)

while True:
    print("hello1")
    frame = tello.get_frame_read().frame  # capturing frame from drone 
    print("hello2")
    diff_x, diff_y = detect_face(frame, display=True)
    
    tello.send_rc_control(int(-diff_x/4), 0, int(diff_y/4), 0)
    
    if cv.waitKey(1) & 0xFF == ord('q'):  # quit from script
        cap.release()
        cv.destroyAllWindows()
        tello.land()
        break