import threading
from time import sleep
import SchcConfig
import ServerSend
import stats.statsct

class ClientThread(threading.Thread):

    def __init__(self, ipClient, portClient, clientSocket, configuration):
        threading.Thread.__init__(self)
        self.configuration = configuration
        self.protocol = None
        self.ipClient = ipClient
        self.portClient = portClient
        self.clientSocketInServer = clientSocket
        self.serverSend = ServerSend.ServerSend(self.clientSocketInServer)
        self.clientConfigInServer = SchcConfig.SchcConfig(self.configuration, self.clientSocketInServer)
        self.iteration = 0
        self.client_config()
        print("[+] Nouveau thread pour %s %s" % (ipClient, portClient,))

    def run(self):
        while True:
            print("Ready to receive a message")

            try:
                fragment1 = self.clientSocketInServer.recv(2048)
                print("--------------------Yo recibi esto: ",fragment1)
                sleep(0.1)
            except:
                print("Not ready to read")
                return

            try:
                d = fragment1.decode()
                print("--------------------Yo decodifiqué esto: ", d)
                if d == "":
                    return
                else:
                    self.recv_message(fragment1)
            except:
                self.recv_message(fragment1)


            self.protocol = self.clientConfigInServer.node0.protocol

            try:
                state = self.protocol.reassemble_session.session_list[0]['session'].state
                print("STATE : ", state)
            except:
                print("Not fragment state ")
                print("--------------------------- End Iteration ", self.iteration, " --------------------------")
                self.client_config()


            if state == 'DONE':
                self.send_message_from_socket(-1)
                print("--------------------------- End Iteration ", self.iteration, " --------------------------")
                self.client_config()
            elif state == 'ERROR_MIC':
                self.send_message_from_socket(0)
                self.protocol.reassemble_session.session_list[0]['session'].state = 'INIT'
            elif state == 'ACK_REQ':
                self.send_message_from_socket(-1)
                self.protocol.reassemble_session.session_list[0]['session'].state = 'INIT'
            elif state == 'ABORT':
                self.send_message_from_socket(0)
                print("--------------------------- End Iteration ", self.iteration, " --------------------------")
                self.client_config()

        self.clientSocketInServer.close()

    def client_config(self):
        self.iteration += 1
        print("")
        print("")
        print("--------------------------- Iteration ", self.iteration, " --------------------------")
        print("---------- Client: Ip = ", self.ipClient, " Port = ", self.portClient, "---------------")
        stats.statsct.Statsct.initialize()
        self.clientConfigInServer.configSim()

    def recv_message(self, fragment):
        print("------------------------------- RECEIVE PACKET ------------------------------")
        print("Fragment received from client: ", fragment)
        self.clientConfigInServer.node0.protocol.layer2.event_receive_packet(self.clientConfigInServer.node0.id,
                                                                             fragment)
    def send_message_from_socket(self, position_queue):
        queue_list = self.protocol.scheduler.queue
        print("queue_list", queue_list)
        message = bytearray(self.protocol.scheduler.queue[position_queue][3][0])
        print("Message server to client", message)
        Bytes = self.clientSocketInServer.send(message)
        print("Sent Bytes:", Bytes)
        sleep(1)