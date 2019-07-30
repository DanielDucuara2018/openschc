import threading
import time

class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket,  schc_config):

        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        self.schc_config = schc_config
        self.protocol = None
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port,))

    def run(self):
        while True:
            print("Ready to receive a message")

            try:
                 fragment1 = self.clientsocket.recv(2048)
                 time.sleep(1)
            except:
                print("Not ready to read")
                return

            try:
                fragment1.decode()
                return
            except:
                self.schc_config.recvMessage(fragment1)


            self.protocol = self.schc_config.node0.protocol

            try:
                state = self.protocol.reassemble_session.session_list[0]['session'].state
                print("STATE : ", state)
            except:
                print("Not fragment state ")
                print("--------------------------- End Iteration  --------------------------")
                self.schc_config.configSim()
                # self.clientsocket.close()
                time.sleep(1)
                # return

            if state == 'DONE':
                message = bytearray(self.protocol.scheduler.queue[0][3][0])
                # self.schc_config.sendMessage(message)
                # self.schc_config.sim.run()
                print("Message server to client",message)
                self.clientsocket.send(message)
                ###print("---------------------------------------------------------------------")
                print("--------------------------- End Iteration  --------------------------")
                #self.clientsocket.close()
                #print("Client déconnecté...")
                #self.protocol.layer2.server.tcpsock.close()
                #print("Server déconnecté...")
                self.schc_config.configSim()
                #break

        self.clientsocket.close()
