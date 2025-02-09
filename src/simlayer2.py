"""
.. module:: simlayer2
   :platform: Python, Micropython
"""
#---------------------------------------------------------------------------
from stats.statsct import Statsct

class SimulLayer2:
    """
    The layer 2 of LPWA is not symmetry.
    The LPWA device must know the devaddr assigned to itself before processing
    the SCHC packet.
    The SCHC gateway must know the devaddr of the LPWA device before
    transmitting the message to the NS.  And, it must know the devaddr
    when it receives the message from the NS.
    Therefore, in this L2 simulation layer, the devaddr must be configured
    before it starts by calling set_devaddr().
    """
    __mac_id_base = 0

    def __init__(self, sim = None):
        self.sim = sim
        self.protocol = None
        self.devaddr = None
        self.mac_id = SimulLayer2.__get_unique_mac_id()
        self.receive_function = None
        self.event_timeout = None
        self.counter = 1 # XXX: replace with is_transmitting?
        self.is_transmitting = False
        self.packet_queue = []
        self.mtu = 56
        self.role = None
        self.roleSend = None

    def set_role(self, role, roleSend):
        self.role = role
        self.roleSend = roleSend

    def _set_protocol(self, protocol):
        self.protocol = protocol
        Statsct.addInfo('protocol', protocol.__dict__)

    def set_receive_callback(self, receive_function):
        self.receive_function = receive_function

    def send_packet(self, packet, dev_L2addr, transmit_callback=None, receive = False):
        self.packet_queue.append((packet, self.mac_id, None,
                                  transmit_callback, receive))
        if not self.is_transmitting:
            self._send_packet_from_queue()

    def _send_packet_from_queue(self):
        assert not self.is_transmitting
        assert len(self.packet_queue) > 0

        self.is_transmitting = True
        (packet, src_dev_id, dst_dev_id, transmit_callback, receive) = self.packet_queue.pop(0)
        print(transmit_callback, "AAAAAAA")
        print("send packet from queue -> {}, {}, {}, {}".format(packet, src_dev_id, dst_dev_id, transmit_callback))

        if self.role == "client" or self.role == "server":
            self.sim.send_packetX(packet, src_dev_id, dst_dev_id, self._event_sent_callback, (transmit_callback,))
        else:
            self.sim.send_packet(packet, src_dev_id, dst_dev_id, self._event_sent_callback, (transmit_callback,))

    def _event_sent_callback(self, transmit_callback, status):
        assert self.is_transmitting
        self.is_transmitting = False
        if transmit_callback != None:
            transmit_callback(status)

    def event_receive_packet(self, other_mac_id, packet):
        print("Address",self.devaddr)
        assert self.protocol != None
        assert self.devaddr is not None
        self.protocol.schc_recv(self.devaddr, packet)

    @classmethod
    def __get_unique_mac_id(cls):
        result = cls.__mac_id_base
        cls.__mac_id_base += 1
        return result

    def set_devaddr(self, devaddr):
        self.devaddr = devaddr

    def set_mtu(self, mtu):
        self.mtu = mtu

    def get_mtu_size(self):
        return self.mtu

#---------------------------------------------------------------------------
