from base_import import *

import SchcConfig
import stats.statsct
import ClientSend

import socket
from time import sleep

class ClientConnection:

	def __init__(self, role, ipServer, portServer, size_message, l2_mtu):
		self.size_message = size_message
		self.size_l2_mtu = l2_mtu
		self.role = role
		self.ipServer = ipServer
		self.portServer = portServer
		self.socketClientConnection = None
		self.clientConfig = None
		self.clientSend = None

	def connection(self):
		self.socketClientConnection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		# connect to server on local computer
		print("Waiting for a server")
		while self.socketClientConnection.connect_ex((self.ipServer, self.portServer)) != 0:
			sleep(0.1)
		print("Conneted to server")
		self.clientSend = ClientSend.ClientSend(self.socketClientConnection)

	def client_config(self):
		stats.statsct.Statsct.initialize()
		self.clientConfig = SchcConfig.SchcConfig(self.role, self.size_l2_mtu, self.clientSend)

	def send_message(self):

		payload = bytearray(range(1, 1 + self.size_message))  # 14 bytes
		print("Payload size:", len(payload))
		print("Payload: {}".format(b2hex(payload)))
		print("")

		self.clientConfig.node0.protocol.layer3.send_later(1, 1, payload)
		self.clientConfig.sim.run()

	def client(self):
		iteration = 1
		while True:
			print("")
			print("--------------- Iteration: ", iteration, " -----------------------")
			self.send_message()
			self.clientConfig.configSim()
			# self.schc_config.node0.protocol.layer2.set_role(self.role)
			sleep(10)
			iteration += 1

		# close the connection 
		#self.socketClientConnection.close()
