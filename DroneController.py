import logging
import socket
import sys
import threading
import time
import cv2 as cv

class Tello(object):
    
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    LOGGER = logging.getLogger('PyTello')    
    background_frame_read = None
    
    # Video stream, server socket
    VS_UDP_IP = '0.0.0.0'
    VS_UDP_PORT = 11111
    
    CONTROL_UDP_PORT = 8889
    STATE_UDP_PORT = 8890
    
    def __init__(self, controller_ip='192.168.10.2', controller_port=8889,
                 drone_ip='192.168.10.1', drone_port=8889):
        print("Initialize Drone Controller")
        self.controller_ip = controller_ip
        self.controller_port =  controller_port
        self.controller_address = (self.controller_ip, self.controller_port)
        
        self.drone_ip = drone_ip
        self.drone_port = drone_port
        self.drone_address = (drone_ip, drone_port)
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(self.controller_address)
                
        self.stream_on = False
        
        self.response = None
        self.stop_event = threading.Event()
        
        self.response_thread = threading.Thread(target=self.receive_response,
                                           args = (self.stop_event, ))
        
        self.response_thread.start()
        
        self.command()
        self.streamon()
        
    
    def get_frame_read(self) -> 'BackgroundFrameRead':
        """Get the BackgroundFrameRead object from the camera drone. Then, you just need to call
        backgroundFrameRead.frame to get the actual frame received by the drone.
        Returns:
            BackgroundFrameRead
        """
        if self.background_frame_read is None:
            self.background_frame_read = BackgroundFrameRead(self, self.get_udp_video_address()).start()
        return self.background_frame_read
    
    def get_udp_video_address(self) -> str:
        """Internal method, you normally wouldn't call this youself.
        """
        return 'udp://@' + self.VS_UDP_IP + ':' + str(self.VS_UDP_PORT)  # + '?overrun_nonfatal=1&fifo_size=5000'
    
    def receive_response(self, stop_event):
        while not stop_event.is_set():
            try:
                self.response, ip = self.socket.recvfrom(3000)
                self.LOGGER.info({'action': 'receive_response',
                             'response': self.response})
    
            except socket.error as ex:
                self.LOGGER.error({'action': 'receive_response',
                              'ex': ex})
                break
            
    
    def stop_connection(self):
        self.LOGGER.info({'action': 'stop_connection'})
        self.stop_event.set() #stop receiving response when closing connection
        
        retry = 0
        while self.response_thread.isAlive():
            time.sleep(0.3)
            if retry > 30:
                break
            retry+=1
            
        self.streamoff()
        self.socket.close()
            
    def send_command(self, command):
        self.LOGGER.info({'action': 'send_command', 'command': command})
        self.socket.sendto(command.encode('utf-8'), self.drone_address)
        
        retry = 0
        while self.response_thread.isAlive():
            time.sleep(0.3)
            if retry > 3:
                break
            retry+=1
            
        if self.response is None:
            response = None
        else:
            response = self.response.decode('utf-8')
            
        self.response= None
        
        return response
    
    # sending command
    def command(self):
        self.send_command('command')

    def takeoff(self):
        return self.send_command('takeoff')
            
    def land(self):
        return self.send_command('land')
    
    def emergency(self):    
        self.send_command('emergency')    
    
    def streamon(self):
        self.send_command('streamon')
        self.stream_on = True
        
    def streamoff(self):
        self.send_command('streamoff')
        self.stream_off = False
    
    # asking for states
    def battery(self):
        return self.send_command('battery?')
    
    def time(self):
        return self.send_command('time?')
        
    def __del__(self):
        self.stop_connection()
        
class BackgroundFrameRead:
    """
    This class read frames from a VideoCapture in background. Use
    backgroundFrameRead.frame to get the current frame.
    """

    def __init__(self, tello, address):
        tello.cap = cv.VideoCapture(address)
        self.cap = tello.cap

        if not self.cap.isOpened():
            self.cap.open(address)

        self.grabbed, self.frame = self.cap.read()
        self.stopped = False

    def start(self):
        threading.Thread(target=self.update_frame, args=(), daemon=True).start()
        return self

    def update_frame(self):
        while not self.stopped:
            if not self.grabbed or not self.cap.isOpened():
                self.stop()
            else:
                (self.grabbed, self.frame) = self.cap.read()

    def stop(self):
        self.stopped = True
        
