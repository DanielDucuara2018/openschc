from base_import import *

import simul
import rulemanager

class SchcConfig:
    def __init__(self, role , size_l2_mtu, clientSend = None):
        self.role = role
        self.size_l2_mtu = size_l2_mtu
        self.clientSend = clientSend
        self.cont = 0
        self.loss_config = None
        self.rule = []
        self.node0 = None
        self.context ="example/context-100.json"
        self.rule_comp = "example/comp-rule-100.json"
        self.rule_fragin2 = "example/frag-rule-201.json"      #NoACK
        self.rule_fragout2 = "example/frag-rule-202.json"     #NoACK
        self.rule_fragin = "example/frag-rule-101.json"      #ACK-ON-Error
        self.rule_fragout = "example/frag-rule-102.json"     #ACK-ON-Error
        self.configRuleManager()
        self.configSim()

    def configRuleManager(self):
        for k in [self.context,self.rule_comp,self.rule_fragin,self.rule_fragout,self.rule_fragin2,self.rule_fragout2]:
            with open(k) as fd:
                self.rule.append(json.loads(fd.read()))

        self.rule_manager = rulemanager.RuleManager()
        if self.role == "client":
            self.rule_manager.add_context(self.rule[0], self.rule[1], self.rule[2], self.rule[3])
        elif self.role == "server":
            self.rule_manager.add_context(self.rule[0], self.rule[1], self.rule[3], self.rule[2])

    def configSim(self):

        self.simul_config = {
            "log": True,
        }

        self.sim = simul.Simul(self.simul_config)

        devaddr = b"\xaa\xbb\xcc\xdd"
        self.node0 = self.make_node(self.sim, self.rule_manager, devaddr)
        self.node0.layer2.set_mtu(self.size_l2_mtu)
        self.node0.layer2.set_role(self.role, self.clientSend)

        print("-------------------------------- SCHC ",self.role," ------------------------")
        print("SCHC device L3={} L2={} RM={}".format(self.node0.layer3.L3addr, self.node0.id,
                                                     self.rule_manager.__dict__))

    def make_node(self, sim, rule_manager, devaddr=None, extra_config={}):
        node = simul.SimulSCHCNode(sim, extra_config)
        node.protocol.set_rulemanager(rule_manager)
        if devaddr is None:
            devaddr = node.id
        node.layer2.set_devaddr(devaddr)
        return node