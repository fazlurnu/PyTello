import logging
import socket
import sys
import threading
import time

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
LOGGER = logging.getLogger('PyTello')

class Tello(object):
    
    
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
                
    def command(self):
        self.send_command('command')
        
    def streamon(self):
        self.send_command('streamon')
        self.stream_on = True
        
    def streamoff(self):
        self.send_command('streamoff')
        self.stream_off = False
    
    def emergency(self):
        self.send_command('emergency')
        
    def receive_response(self, stop_event):
        while not stop_event.is_set():
            try:
                self.response, ip = self.socket.recvfrom(3000)
                LOGGER.info({'action': 'receive_response',
                             'response': self.response})
    
            except socket.error as ex:
                LOGGER.error({'action': 'receive_response',
                              'ex': ex})
                break
            
    
    def stop_connection(self):
        LOGGER.info({'action': 'stop_connection'})
        self.stop_event.set() #stop receiving response when closing connection
        
        retry = 0
        while self.response_thread.isAlive():
            time.sleep(0.3)
            if retry > 30:
                break
            retry+=1
            
        self.socket.close()
            
    def send_command(self, command):
        LOGGER.info({'action': 'send_command', 'command': command})
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
    
    def battery(self):
        return self.send_command('battery?')
            
    def takeoff(self):
        return self.send_command('takeoff')
            
    def land(self):
        return self.send_command('land')
    
    def __del__(self):
        self.stop_connection()
        

        
        
        
        