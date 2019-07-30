from time import sleep
import socket

class ClientConnection():


    def __init__(self,ip, portIp):
      self.soc = None
      self.ip = ip
      self.portIp = portIp
      self.socketcomunication()

    def socketcomunication(self):
      self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      # self.soc.connect((ip, port))
      print("Waiting for a server")
      while self.soc.connect_ex((self.ip, self.portIp)) != 0:
        sleep(0.1)
      print("Conneted to server")


    def send(self, message):
      print("Message to Server", message)
      self.soc.send(message)
      sleep(1)
      #messageRecvd = self.ReceiveUntil(1)
      #return messageRecvd

    def Receive(self):
      currentMsg = ''
      try:
        print("Ready to receive a message")
        currentMsg = self.soc.recv(2048)
      except:
        print("Any message from server")
      sleep(1)
      return currentMsg

      # # if self.verbosity >= 2: ("       #method ReceiveUntil")
      # iterCount = timeOut / 0.15
      # #		self.ser.timeout = 0.1
      # currentMsg = ''
      # status = ''
      # while iterCount >= 0 and "SUCCESS" not in status:
      #   sleep(0.1)
      #   #			while self.ser.inWaiting() > 0 : # bunch of data ready for reading
      #   currentMsg = self.soc.recv(2048)
      #   if currentMsg != '':
      #     status = "SUCCESS"
      #   iterCount -= 1
      #   print("Message from Server", currentMsg)
      #
      # if currentMsg != b"SUCCESS":
      #   return currentMsg
      # return ''

    def close(self):
      if self.ser.isOpen():
        self.ser.close()
