import numpy as np
import cv2 as cv
from time import time, sleep

import logging
import socket
import sys

#logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#logger = logging.getLogger(__name__)

class DroneManager(object):
    def __init__(self, host_ip='192.168.10.2', host_port=8889,
                 drone_ip='192.168.10.1', drone_port=8889):
        self.host_ip = host_ip
        self.host_port = host_port
        self.drone_ip = drone_ip
        self.drone_port = drone_port
        self.drone_address = (drone_ip, drone_port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host_ip, self.host_port))
        self.socket.sendto(b'command', self.drone_address)
        self.socket.sendto(b'streamon', self.drone_address)

    def __dell__(self):
        self.stop()

    def stop(self):
        self.socket.close()

    def send_command(self, command):
        logger.info({'action': 'send_command', 'command': command})
        self.socket.sendto(command.encode('utf-8'), self.drone_address)

    def takeoff(self):
        self.send_command('takeoff')

    def land(self):
        self.send_command('land')
        
class CameraMorse:
    """
        Designed with the Tello drone in mind but could be used with other small cameras.
        When the Tello drone is not flying, we can use its camera as a way to pass commands to the calling script.
        Covering/uncovering the camera with a finger, is like pressing/releasing a button. 
        Covering/uncovering the camera is determined by calculating the level of brightness of the frames received from the camera
        Short press = dot
        Long press = dash
        If we associate series of dots/dashes to commands, we can then ask the script to launch these commands.
    """
    def __init__(self, dot_duration=0.2, dash_duration=None, blank_duration=None, display=False, threshold=40):
        """
            display : True to display to display brightness(time) in an opencv window (via an object RollingGraph)
        """
        # Durations below are in seconds
        # 0 < duration of a dash <= dot_duration 
        self.dot_duration = dot_duration
        # dot_duration < duration of a dash <= dash_duration
        if dash_duration is None:
            self.dash_duration = 3*dot_duration
        else:
            self.dash_duration = dash_duration
        # Released duration. 
        if blank_duration is None:
            self.blank_duration = 3*dot_duration
        else:
            self.blank_duration = blank_duration

        # Dots or dashes are delimited by a "press" action followed by a "release" action
        # In normal situation, the brightness is above 'threshold'
        # When brightness goes below 'threshold' = "press" action
        # Then when brightness goes back above 'threshold' = "release" action
        self.threshold = threshold

        # Dictionary that associates codes to commands 
        self.commands = {}

        # Current status 
        self.is_pressed = False

        # Timestamp of the last status change (pressed/released)
        self.timestamp = 0

        # Current morse code. String composed of '.' and '-'
        code=""

        self.display = display

    def define_command(self, code, command, kwargs={}):
        """
            Add a (code, command, args) to the dictionary of the command
            'command' is a python function
            kwargs is a optionnal dictionary of keyword arguments that will be passed to function 'command' 
            when it will be called. Called this way: command(**kwargs)
            Beware that if code1 is a prefix of code2, the command associated to code2 will never be called !
        """
        self.commands[code] = (command, kwargs)

    def is_pressing (self, frame):
        """
            Calculate the brightness of a frame and 
            returns True if the brightness is below 'threshold' (= pressing)
        """
        self.brightness = np.mean(frame)
        
        return self.brightness < self.threshold

    def check_command(self):
        cmd, kwargs = self.commands.get(self.code, (None,None))
        if cmd: # We have a code corresponding to a command -> we launch the command
            cmd(**kwargs)
            self.code = ""

    def eval(self,frame):
        """
            Analyze the frame 'frame', detect potential 'dot' or 'dash', and if so, check 
            if we get a defined code
            Returns:
            - a boolean which indicates if the "button is pressed" or not,
            - "dot" or "dash"  if a dot or a dash has just been detected, or None otherwise
        """
        if not self.commands: return None

        pressing = self.is_pressing(frame)
        current_time = time()

        detected = None
        if self.is_pressed and not pressing: # Releasing
            if current_time - self.timestamp < self.dot_duration: # We have a dot
                self.code += "."
                detected = "dot"
                self.check_command()
            elif current_time - self.timestamp < self.dash_duration: # We have a dash
                self.code += "-"
                detected = "dash"
                self.check_command()
            else: # The press was too long, we cancel the current decoding
                self.code = ""
            self.is_pressed = False
            self.timestamp = current_time
        elif not self.is_pressed and pressing: # Pressing
            if current_time - self.timestamp > self.blank_duration: # The blank was too long, we cancel the current decoding
                self.code = ""
            self.is_pressed = True
            self.timestamp = current_time
        
        return pressing, detected

if __name__ == "__main__":

    def test(arg):
        print(arg)
        if arg=="Delayed Take-off":
            current_time = time()
            delay_duration = 10
            
            if (current_time - cm.timestamp > delay_duration):
                print("Go take off!")
            cm.timestamp = current_time
            #drone_manager.takeoff()
            #time.sleep(1)

            #drone_manager.land()
        elif arg=="Throw and Fly":
            sleep(2)
            print("Hand take off!")
            


    cap = cv.VideoCapture(0)
    
    cm = CameraMorse(dot_duration=0.5, display=True)
    cm.define_command("..", test, {"arg": "Delayed Take-off"})
    cm.define_command(".-", test, {"arg": "Throw and Fly"})
    
    #drone_manager = DroneManager()
    
    #print("Ready to take off")
    #time.sleep(5)
    
    #drone_manager.takeoff()

    
    while True:
        ret, frame = cap.read()
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        print(cm.eval(gray))
        cv.imshow('frame', gray)
        
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        
    cv.destroyAllWindows()
    cap.release()