import sys

import argparse

import ClientConnection
import ServerConnection

class ClientServerSimul:

    def __init__(self, role):
        self.configuration = {}
        self.config(role)
        self.client = None
        self.server = None

    def config(self, role):
        self.configuration['role'] = role
        self.configuration['ipServer'] = "127.0.0.1"
        self.configuration['portServer'] = 12345
        self.configuration['l2_mtu'] = 408# In bits
        self.configuration['size_message'] = 255# In bytes
        self.configuration['ack_on_error'] = True
        self.configuration['time_between_iteration'] = 10
        self.configuration['packet_loss_simulation'] = False
        self.configuration['payload_file_simulation'] = True
        self.configuration['payload_name_file'] = "testfile_large.txt"

    def start(self):
        if self.configuration['role'] == "client":
            print("")
            self.client = ClientConnection.ClientConnection(self.configuration)
            self.client.connection()
            self.client.client()
        elif self.configuration['role'] == "server":
            print("")
            self.server = ServerConnection.ServerConnection(self.configuration)
            self.server.connection()
            self.server.server()

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

schcConfig = ClientServerSimul(role)
schcConfig.start()
#-----------------------------------------------------------------------
