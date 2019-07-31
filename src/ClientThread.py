import threading
import time
import SchcConfig

class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientSocket, role, size_l2_mtu):
        threading.Thread.__init__(self)
        self.protocol = None
        self.ip = ip
        self.port = port
        self.role = role
        self.size_l2_mtu = size_l2_mtu
        self.clientSocketInServer = clientSocket
        self.clientConfigInServer = self.client_config()
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port,))

    def run(self):
        while True:
            print("Ready to receive a message")

            try:
                fragment1 = self.clientSocketInServer.recv(2048)
                time.sleep(1)
            except:
                print("Not ready to read")
                return

            try:
                fragment1.decode()
                return
            except:
                self.recv_message(fragment1)


            self.protocol = self.clientConfigInServer.node0.protocol

            try:
                state = self.protocol.reassemble_session.session_list[0]['session'].state
                print("STATE : ", state)
            except:
                print("Not fragment state ")
                print("--------------------------- End Iteration  --------------------------")
                self.clientConfigInServer.configSim()
                # self.clientsocket.close()
                time.sleep(1)
                # return

            if state == 'DONE':
                message = bytearray(self.protocol.scheduler.queue[0][3][0])
                # self.schc_config.sendMessage(message)
                # self.schc_config.sim.run()
                print("Message server to client",message)
                self.clientSocketInServer.send(message)
                ###print("---------------------------------------------------------------------")
                print("--------------------------- End Iteration  --------------------------")
                #self.clientsocket.close()
                #print("Client déconnecté...")
                #self.protocol.layer2.server.tcpsock.close()
                #print("Server déconnecté...")
                self.clientConfigInServer.configSim()
                #break

        self.clientSocketInServer.close()

    def client_config(self):
        client_config = SchcConfig.SchcConfig(self.role, self.size_l2_mtu)
        return client_config

    def recv_message(self,Fragment):
        print("Fragment receiverd: ",Fragment)
        self.clientConfigInServer.node0.protocol.layer2.event_receive_packet(self.clientConfigInServer.node0.id, Fragment)