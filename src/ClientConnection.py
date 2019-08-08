import SchcConfig
import stats.statsct
import ClientSend

import socket
from time import sleep

class ClientConnection:

	# def __init__(self, role, ipServer, portServer, l2_mtu, size_message):
	def __init__(self, configuration):
		self.configuration = configuration
		self.socketClientConnection = None
		self.clientConfig = None
		self.clientSend = None

	def connection(self):
		self.socketClientConnection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		# connect to server on local computer
		print("Waiting for a server")
		while self.socketClientConnection.connect_ex((self.configuration['ipServer'], self.configuration['portServer'])) != 0:
			sleep(0.1)
		print("Conneted to server")
		self.clientSend = ClientSend.ClientSend(self.socketClientConnection)
		self.clientConfig = SchcConfig.SchcConfig(self.configuration, self.clientSend)

	def client_config(self, iteration):
		print("")
		print("")
		print("--------------- Iteration: ", iteration, " -----------------------")
		stats.statsct.Statsct.initialize()
		self.clientConfig.configSim()

	def send_message(self):
		payload = self.clientConfig.config_packet()
		self.clientConfig.node0.protocol.layer3.send_later(1, 1, payload)
		self.clientConfig.sim.run()

	def client(self):
		iteration = 1
		while True:
			self.client_config(iteration)
			self.send_message()
			print("--------------- End iteration: ", iteration, " -----------------------")
			sleep(self.configuration['time_between_iteration'])
			iteration += 1

