# import socket programming library
from base_import import *

import socket
import ClientThread

# print_lock = threading.Lock()

class ServerConnection:

    def __init__(self, configuration):
        self.configuration = configuration
        self.socketServerConnection = None
        self.clientSocket = None
        self.newThread = None
        self.serverSend = None

    def connection(self):
        self.socketServerConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# IP4
        self.socketServerConnection.bind((self.configuration['ipServer'], self.configuration['portServer']))
        print("socket binded to ", self.configuration['ipServer'], " ip and port ", self.configuration['portServer'])

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
            self.newThread = ClientThread.ClientThread(ipClient, portClient, self.clientSocket, self.configuration)
            self.newThread.start()

