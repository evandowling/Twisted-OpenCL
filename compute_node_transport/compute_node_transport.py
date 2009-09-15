from twisted.internet import defer, protocol, reactor
from twisted.protocols import basic
from compute_core import *

class ComputeNodeTransportProtocol(protocol.Protocol):
    DELIMITER = ';;end;;'
    def connectionMade(self):
        print "Connection Made"
        self.factory.addServer(self.transport.getPeer())
        self.buf = []
        
    def dataReceived(self, data):
        self.buf += data
        self.parseBuffer()
        
    def connectionLost(self,data):
        """ 
        When we lose our connection to the simulation manager, we notify the compute core that we are ready to receive work again.
        """
        self.factory.notifySynchronizerLost(self.transport.getPeer())
        
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
                elif packet[0:3] == 'TRFM':
                    self.factory.setTransform(packet[4:idx])
                elif packet[0:3] == 'COMP':
                    self.factory.performComputation(self.transport)                 
                else:
                    print "%s is a malformed packet, header %s not recognized" % (packet, packet[0:3])
            else:
                print "%s attempting to send a packet of invalid length %s" % (packet, len(packet))
            self.buf = self.buf[(idx + len(DELIMITER)):]
            idx = self.buf.find(DELIMITER)
            

class ComputeNodeTransportFactory(protocol.ServerFactory):
    protocol = ComputeNodeTransportProtocol
    def __init__(self, computation_core):
        self.computation_core = computation_core
        
    def setTransform(self, transform):
        self.computation_core.setTransform(transform)
    
    def setData(self, data):
        self.computation_core.setData(data)
        
    def performComputation(self,transport):
        transport.write(self.computation_core.performTransform())
    
    def notifySynchronizerLost(simulation_manager):
        self.computation_core.lostManager(simulation_manager)
                                          

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

    protocol = ComputeNodeManagementClient

    def clientConnectionFailed(self, _, reason):
        pass

    def gotData(self, data):
        print data
    