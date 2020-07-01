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
        print('faces detected')
        for i, (x, y, w, h) in enumerate(faces):
            cv.rectangle(frame, (x, y), (x+w, y+h), BLUE, 2)
            
            center_face = (int(x + w/2), int(y + h/2))
                    
            cv.line(frame, center, center_face, RED, 2)
            cv.circle(frame, center_face, 5, RED, 2)
            
            cv.putText(frame, "id: " + str(i+1), (x, y-10), cv.FONT_HERSHEY_SIMPLEX,  
                           0.5, BLUE, 2, cv.LINE_AA)
    else:
        print('faces not detected')
        
    if(display):
        cv.imshow('frame', frame)
        
    #diff_x = center[0] - center_face[0]
    #diff_y = center[1] - center_face[1]

        
    #return diff_x, diff_y
        
    
def main():
    while True:
        ret, frame = cap.read()
        detect_face(frame, display=True)
        
        #print(diff_x, diff_y)
        
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        

if __name__ == "__main__":
    main()
    cap.release()
    cv.destroyAllWindows()
    
