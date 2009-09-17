from twisted.internet import defer, protocol, reactor
from twisted.protocols import basic
from compute_core import *

class ComputeNodeTransportProtocol(protocol.Protocol):
    DELIMITER = ';;end;;'
    def connectionMade(self):
        print "Connection Made"
        self.buf = []
        
    def dataReceived(self, data):
        self.buf += data
        self.parseBuffer()
        
    def connectionLost(self,data):
        pass
        
    def parseBuffer(self):
        """ 
        Chomp off complete packets one at a time communicate their contents through the factory to the compute core.
        """
        idx = self.buf.find(DELIMITER)
        while idx > -1:
            packet = self.buf[0:idx]
            if len(packet) > 4:
                if packet[0:3] == 'DATA':
                    self.factory.setData(packet[4:idx])
                else:
                    print "%s is a malformed packet, header %s not recognized" % (packet, packet[0:3])
            else:
                print "%s attempting to send a packet of invalid length %s" % (packet, len(packet))
            self.buf = self.buf[(idx + len(DELIMITER)):]
            idx = self.buf.find(DELIMITER)
            

class ComputeNodeTransportFactory(protocol.ServerFactory):
    protocol = ComputeNodeTransportProtocol
    def __init__(self,simulation_manager):
        """
        Set up the initial data pathways
        """
        self.simulation_manager = simulation_manager
    
    def setData(self, data):
        self.simulation_manager.setData(data)
                                          
"""
The client is what acutally sits on the postman server.  
It connects to a compute node running a transport server and synchronizes computation.
"""
class ComputeNodeTransportClient(protocol.Protocol):

    def connectionMade(self):
        print "Connection Made"
        self.buf = []

    def dataReceived(self, data):
        print data
        
    def connectionLost(self, reason):
        print "Connection Closed"

class ComputeNodeTransportClientFactory(protocol.ClientFactory):

    protocol = ComputeNodeTransportClient
    def __init__(self,compute_core):
        """
        Set up the initial data pathways
        """
        self.compute_core = compute_core
        
    def clientConnectionFailed(self, _, reason):
        pass

    def setData(self, data):
        self.compute_core.sendData(data)
        