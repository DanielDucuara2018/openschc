import socket

class ServerConnection:
    def __init__(self,ip, portIp):
        try:
            self.tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #self.tcpsock = socket.socket()
            self.tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.tcpsock.bind((ip, portIp))
        except:
            print("Server already active")
