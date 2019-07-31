# import socket programming library
from base_import import *

import socket
import ClientThread
# print_lock = threading.Lock()

class ServerConnection:

    def __init__(self, role, ipServer, portServer, size_l2_mtu):
        self.size_l2_mtu = size_l2_mtu
        self.ip = ipServer
        self.port = portServer
        self.role = role
        self.socketServerConnection = None
        self.clientSocket = None
        self.newThread = None

    def connection(self):
        self.socketServerConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketServerConnection.bind((self.ip, self.port))
        print("socket binded to port", self.port)

    def server(self):
        # a forever loop until client wants to exit# put the socket into listening mode
        while True:

            self.socketServerConnection.listen(10)
            print("socket is listening")

            # establish connection with client
            (self.clientSocket, (ipClient, portClient)) = self.socketServerConnection.accept()

            # lock acquired by client
            # print_lock.acquire()
            print("Connexion de %s %s" % (ipClient, portClient,))

            # Start a new thread and return its identifier

            self.newThread = ClientThread.ClientThread(ipClient, portClient, self.clientSocket, self.role, self.size_l2_mtu)
            self.newThread.start()

