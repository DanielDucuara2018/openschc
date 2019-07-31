
from time import sleep

class ClientSend:

    def __init__(self, socketClientConnection):
        self.socketClientConnection = socketClientConnection

    def send(self, message):
      print("Message to Server", message)
      self.socketClientConnection.send(message)
      sleep(1)
      #messageRecvd = self.ReceiveUntil(1)
      #return messageRecvd

    def Receive(self):
      currentMsg = ''
      try:
        print("Ready to receive a message")
        currentMsg = self.socketClientConnection.recv(2048)
      except:
        print("Any message from server")
      sleep(1)
      return currentMsg