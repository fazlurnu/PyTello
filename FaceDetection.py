import cv2 as cv

cap = cv.VideoCapture(0)

face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
RED = (0, 0, 255)
BLACK = (0, 0, 0)
    
def detect_face(frame, display = False):
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    frame_height = frame.shape[0]
    frame_width = frame.shape[1]
    
    center = (int(frame_width/2), int(frame_height/2))
    #print(frame_widht, frame_height)
    
    cv.circle(frame, center, 5, RED, 2)
    
    if (len(faces) > 0):
        is_deteceted = True
    else:
        is_deteceted = False
        
    if is_deteceted:
        for i, (x, y, w, h) in enumerate(faces):
            center_face = (int(x + w/2), int(y + h/2))
            cv.rectangle(frame, (x, y), (x+w, y+h), BLUE, 2)
    
    else:
        center_face = (0,0)
        
    return center_face, is_deteceted
    
def main():
    
    ret, frame = cap.read()
    
    display = True
    
    while True:
        ret, frame_now = cap.read()
        
        # operation
        center_face_now, is_detected_now = detect_face(frame_now, display=True)
        
        if display:
            cv.imshow('frame', frame_now)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break                

if __name__ == "__main__":
    main()
    cap.release()
    cv.destroyAllWindows()
    
