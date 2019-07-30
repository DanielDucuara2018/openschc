from base_import import *
from SchcConfig import SchcConfig
import sys

import argparse
import time

from stats.statsct import Statsct

from ClientThread import ClientThread

from schc import Session

class ClientServerSimul:

    def __init__(self, role):
        self.schc_config = None
        self.role = role
        self.tcpsock = None
        self.stats = Statsct.initialize()
        self.schc_config = SchcConfig(self.role)

    def send_message(self):

        data_size = 255  # bytes
        payload = bytearray(range(1, 1 + data_size))  # 14 bytes
        print("Payload size:", len(payload))
        print("Payload: {}".format(b2hex(payload)))
        print("")

        self.schc_config.sendMessage(payload)
        self.schc_config.sim.run()

    def receive_message(self):

        #self.schc_config.sim.run()
        self.tcpsock = self.schc_config.node0.protocol.layer2.serverConnection.tcpsock

        while True:
            self.tcpsock.listen(10)
            print("En écoute...")
            (clientsocket, (ip, port)) = self.tcpsock.accept()
            print("Connexion de %s %s" % (ip, port,))
            newthread = ClientThread(ip, port, clientsocket, self.schc_config)
            newthread.start()
            # break
            # self.clientsocket.close()


    def start(self):
        if self.role == "client":
            iteration = 1
            while True:
                print("")
                print("--------------- Iteration: ", iteration, " -----------------------")
                self.send_message()
                ClientServerSimul(self.role)
                #self.schc_config.node0.protocol.layer2.set_role(self.role)
                time.sleep(5)
                iteration += 1
        elif self.role == "server":
            self.receive_message()

#-----------------------------------------------------------------------------------
print(sys.argv)
for param in sys.argv:
    print(param)

ap = argparse.ArgumentParser(description="a SCHC simulator.",
                             formatter_class=argparse.ArgumentDefaultsHelpFormatter)
ap.add_argument("--r", action="store", dest="role",
                default="client",
                help="specify a role: client or server.")
opt = ap.parse_args()

print(opt.role)
role = opt.role
#role = "server"

schcConfig = ClientServerSimul(role)
schcConfig.start()
#-----------------------------------------------------------------------
