import sys

import argparse

import ClientConnection
import ServerConnection

class ClientServerSimul:

    def __init__(self, role):
        self.size_message = 255
        self.l2_mtu = 404
        self.ipServer = "127.0.0.1"
        self.portServer = 12345
        self.role = role
        self.client = None
        self.server = None

    def start(self):
        if self.role == "client":
            print("")
            self.client = ClientConnection.ClientConnection(self.role, self.ipServer, self.portServer, self.size_message, self.l2_mtu)
            self.client.connection()
            self.client.client_config()
            self.client.client()
        elif self.role == "server":
            print("")
            self.server = ServerConnection.ServerConnection(self.role, self.ipServer, self.portServer, self.l2_mtu)
            self.server.connection()
            self.server.server()

#-----------------------------------------------------------------------------------
print(sys.argv)
for param in sys.argv:
    print(param)

ap = argparse.ArgumentParser(description="a SCHC simulator.",
                             formatter_class=argparse.ArgumentDefaultsHelpFormatter)
ap.add_argument("--r", action="store", dest="role",
                default="server",
                help="specify a role: client or server.")
opt = ap.parse_args()

print(opt.role)
role = opt.role
#role = "server"

schcConfig = ClientServerSimul(role)
schcConfig.start()
#-----------------------------------------------------------------------
