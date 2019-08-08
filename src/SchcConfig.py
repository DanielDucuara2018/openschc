from base_import import *

import simul
import rulemanager

class SchcConfig:
    def __init__(self, configuration, roleSend = None):
        # self.role = role
        # self.l2_mtu = l2_mtu
        self.configuration = configuration
        self.roleSend = roleSend
        self.rule = []
        self.node0 = None
        self.sim = None
        self.context ="example/context-100.json"
        self.rule_comp = "example/comp-rule-100.json"
        self.rule_fragin2 = "example/frag-rule-201.json"      #NoACK
        self.rule_fragout2 = "example/frag-rule-202.json"     #NoACK
        self.rule_fragin = "example/frag-rule-101.json"      #ACK-ON-Error
        self.rule_fragout = "example/frag-rule-102.json"     #ACK-ON-Error
        self.rule_manager = None
        self.configRuleManager()
        #self.configSim()

    def configRuleManager(self):
        for k in [self.context,self.rule_comp,self.rule_fragin,self.rule_fragout,self.rule_fragin2,self.rule_fragout2]:
            with open(k) as fd:
                self.rule.append(json.loads(fd.read()))

        self.rule_manager = rulemanager.RuleManager()

        if self.configuration['ack_on_error']:
            self.ack_on_error_mode()
        else:
            self.no_ack_mode()

    def ack_on_error_mode (self):
        if self.configuration['role'] == "client":
            self.rule_manager.add_context(self.rule[0], self.rule[1], self.rule[2], self.rule[3])
        elif self.configuration['role'] == "server":
            self.rule_manager.add_context(self.rule[0], self.rule[1], self.rule[3], self.rule[2])

    def no_ack_mode(self):
        if self.configuration['role'] == "client":
            self.rule_manager.add_context(self.rule[0], self.rule[1], self.rule[4], self.rule[5])
        elif self.configuration['role'] == "server":
            self.rule_manager.add_context(self.rule[0], self.rule[1], self.rule[5], self.rule[4])

    def configSim(self):

        simul_config = {
            "log": True,
        }

        # Configuration packets loss
        if self.configuration['packet_loss_simulation']:
            # Configuration with packet loss in noAck and ack-on-error
            loss_rate = 15  # in %
            collision_lambda = 0.1
            background_frag_size = 54
            loss_config = {"mode": "rate", "cycle": loss_rate}
            # loss_config = {"mode":"collision", "G":collision_lambda, "background_frag_size":background_frag_size}
        else:
            # Configuration without packet loss in noAck and ack-on-error
            loss_config = None

        if loss_config is not None:
            simul_config["loss"] = loss_config

        self.sim = simul.Simul(simul_config)

        devaddr = b"\xaa\xbb\xcc\xdd"
        self.node0 = self.make_node(self.sim , self.rule_manager, devaddr)
        self.node0.layer2.set_mtu(self.configuration['l2_mtu'])
        self.node0.layer2.set_role(self.configuration['role'], self.roleSend)

        print("-------------------------------- SCHC ", self.configuration['role'], " ------------------------")
        print("SCHC device L3={} L2={} RM={}".format(self.node0.layer3.L3addr, self.node0.id,
                                                     self.rule_manager.__dict__))

    def make_node(self, sim, rule_manager, devaddr=None, extra_config={}):
        node = simul.SimulSCHCNode(sim, extra_config)
        node.protocol.set_rulemanager(rule_manager)
        if devaddr is None:
            devaddr = node.id
        node.layer2.set_devaddr(devaddr)
        return node

    def config_packet(self):
        if self.configuration['payload_file_simulation']:
            fileToSend = self.configuration['payload_name_file']
            file = open(fileToSend, 'r')  # 1400 bytes
            payload = file.read().encode()
            print("Payload size:", len(payload), "bytes")
            print("Payload: {}".format(b2hex(payload)))
            print("")
        else:
            payload = bytearray(range(1, 1 + self.configuration['size_message']))  # 14 bytes
            print("Payload size:", len(payload))
            print("Payload: {}".format(b2hex(payload)))
            print("")
        return payload

