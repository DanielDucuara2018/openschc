
from time import sleep

class ClientSend:

    def __init__(self, socketClientConnection):
        self.socketClientConnection = socketClientConnection

    def send(self, message):
      print("Message to Server", message)
      Bytes = self.socketClientConnection.send(message)
      print("Sent Bytes:", Bytes)
      sleep(1)

    def Receive(self):
      currentMsg = ''
      sleep(0.1)
      try:
        print("Ready to receive a message")
        currentMsg = self.socketClientConnection.recv(2048)
      except:
        print("Any message from server")
      return currentMsg