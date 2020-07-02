import logging
import socket
import sys
import threading
import time
import cv2 as cv

class Tello(object):
    
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    LOGGER = logging.getLogger('PyTello')    
    
    cap = None
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
        
    def move(self, direction, distance):    
        return self.send_command(direction + ' ' + str(distance))
    
    def move_up(self, distance):
        return self.move('up', distance)
    
    def move_down(self, distance):
        return self.move('down', distance)
    
    def move_left(self, distance):
        return self.move('left', distance)
    
    def move_right(self, distance):
        return self.move('right', distance)
    
    def move_forward(self, distance):
        return self.move('forward', distance)
    
    def move_back(self, distance):
        return self.move('back', distance)
    
    def rotate(self, direction, degrees):
        return self.send_command(direction + ' ' + str(degrees))
    
    def rotate_cw(self, degrees):
        return self.rotate('cw', degrees)
    
    def rotate_ccw(self, degrees):
        return self.rotate('ccw', degrees)
    
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
        
