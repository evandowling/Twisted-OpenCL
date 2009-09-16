from twisted.internet import defer, protocol, reactor
from twisted.protocols import basic
from resource_allocator import *

""" 
I've included this for the purpose of test scripting, in real life we would
access the postman via a webservice.  The webservice is responsible for sanitization of inputs
to prevent security violations.
"""
class SimulationAllocationProtocol(protocol.Protocol):
    DELIMITER = ';;end;;'
    def connectionMade(self):
        print "Connection Made"
        self.buf = []
        
    def dataReceived(self, data):
        pass
        
    def connectionLost(self,data):
        """ 
        When we lose our connection to the simulation manager, we notify the compute core that we are ready to receive work again.
        """

        
    
            

class SimulationAllocationFactory(protocol.ServerFactory):
    protocol = SimulationAllocationProtocol

                                          

"""
The client is what acutally sits on the postman server.  
It connects to a remote host that sends out requests for new simulation resources
"""
class SimulationAllocationClient(protocol.Protocol):
    DELIMITER = ';;end;;'
    def connectionMade(self):
        print "Connection Made"
        self.buf = []

    def dataReceived(self, data):
        """
        On receipt of data, append it to a growing buffer which is parsed on change,
        this will be responsible for triggering allocation of resources and receipt of
        simulation info, initial conditions, transform definitions etc...
        """
        self.buf += data
        self.parseBuffer()
        
    def parseBuffer(self):
        """ 
        Chomp off complete packets one at a time communicate their contents through the factory to the resource allocator
        """
        idx = self.buf.find(DELIMITER)
        while idx > -1:
            packet = self.buf[0:idx]
            if len(packet) > 4:
                if packet[0:3] == 'DATA':
                    self.factory.setInitialConditions(packet[4:idx])
                elif packet[0:3] == 'TRFM':
                    self.factory.setTransform(packet[4:idx])
                elif packet[0:3] == 'COMP':
                    self.factory.performComputation(packet[4:idx])                 
                else:
                    print "%s is a malformed packet, header %s not recognized" % (packet, packet[0:3])
            else:
                print "%s attempting to send a packet of invalid length %s" % (packet, len(packet))
            self.buf = self.buf[(idx + len(DELIMITER)):]
            idx = self.buf.find(DELIMITER)

    def connectionLost(self, reason):
        print "Connection Closed"

class SimulationAllocationClientFactory(protocol.ClientFactory):

    protocol = ComputeNodeManagementClient
    def __init__(self):
        self.resource_allocator = ResourceAllocator()
        
    def clientConnectionFailed(self, _, reason):
        pass

    def setTransform(self,packet):
        self.resource_allocator.setTransform(packet)
        
    def setInitialConditions(self,packet):
        self.resource_allocator.setInitialConditions(packet)
    
    def performComputation(self,simulation_id):
        self.resource_allocator.startSimulation(simulation_id)
    