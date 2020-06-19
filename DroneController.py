import socket
import time
import logging

logger = logging.getLogger(__name__)

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
        
        self.socket.sendto('command'.encode('utf-8'), self.drone_address) #initialize SDK mode
        self.socket.sendto('streamon'.encode('utf-8'), self.drone_address) #initialize video streaming
        
        def __del__(self):
            print("Stopping Connection")
            self.stop_connection()
            
        def stop_connection(self):
            self.socket.close()
            
        def send_command(self, command):
            logger.info({'action': 'send_command', 'command': command})
            self.socket.sendto(command.encode('utf-8'), self.drone_address)
            
        def takeoff(self):
            self.send_command("takeoff")
            
        def land(self):
            self.send_command("land")
        
        
        
        