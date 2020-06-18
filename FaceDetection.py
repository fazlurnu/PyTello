import cv2 as cv

cap = cv.VideoCapture(0)

face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
RED = (0, 0, 255)

while True:
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    

    frame_height = frame.shape[0]
    frame_width = frame.shape[1]
    
    center = (int(frame_width/2), int(frame_height/2))
    #print(frame_widht, frame_height)
    
    cv.circle(frame, center, 5, RED, 2)
    
    for (x, y, w, h) in faces:
        cv.rectangle(frame, (x, y), (x+w, y+h), BLUE, 2)
        
        center_face = (int(x + w/2), int(y + h/2))
        cv.line(frame, center, center_face, RED, 2)
        cv.circle(frame, center_face, 5, RED, 2)

    cv.imshow('frame', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
