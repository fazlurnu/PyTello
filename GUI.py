import tkinter as tk
from PIL import Image, ImageTk
import cv2

def takeoff():
    lbl_value["text"] = "Take off"
    
def landing():
    lbl_value["text"] = "Landing"

window = tk.Tk()

img = cv2.imread('logo.png')
b,g,r = cv2.split(img)
img = cv2.merge((r,g,b))
im = Image.fromarray(img)
imgtk = ImageTk.PhotoImage(image=im) 

while True:
    frame = tk.Frame(master=window, width=900, height=900)
    frame.pack()
    
    btn_TO = tk.Button(master=frame, text="Take Off", command=takeoff)
    btn_TO.place(x=250, y=800)
    
    lbl_value = tk.Label(master=frame, text="Status")
    lbl_value.place(x=450, y=600)
    
    image_label = tk.Label(master=frame, image=imgtk)
    
    btn_LD = tk.Button(master=frame, text="Landing", command=landing)
    btn_LD.place(x=600, y=800)
    
    image_label.pack()
    btn_LD.pack()
    btn_TO.pack()
    window.mainloop()