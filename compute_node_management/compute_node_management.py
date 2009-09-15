from twisted.internet import defer, protocol, reactor
from twisted.protocols import basic

class ComputeNodeManagementProtocol(protocol.Protocol):
    def connectionMade(self):
        print "Connection Made"
        self.factory.addServer(self.transport.getPeer())
        
    def dataReceived(self, data):
        pass
        
    def connectionLost(self,data):
        self.factory.removeServer(self.transport.getPeer())

class ComputeNodeManagementFactory(protocol.ServerFactory):
    protocol = ComputeNodeManagementProtocol
    def __init__(self, resource_allocator = None):
        self.resource_allocator = resource_allocator
        self.servers = {}
        
    def addServer(self, server):
        """ Recieve a hello packet from a new client, add that client to the dict
        of compute resources, set its value to 0 initially, 
        meaning it is not initially assigned to a task """
        server_id = "%s:%s" % (server.host, server.port)
        print "%s has been added to the server farm" % server_id
        self.servers[server_id] = 0
        
    def removeServer(self,server):
        """ Client Node Disconnected, remove this from the list of available resources
        and notify the allocator in case a process was interrupted,
        we are not responsible for knowing that here.
        """
        server_id = "%s:%s" % (server.host, server.port)
        if server_id in self.servers:
            del self.servers[server_id]
            print "%s has been removed from the server farm" % server_id
            if self.resource_allocator is not None:
                self.resource_allocator.notifyServerDown(self.servers,server_id)
        
    def getServers(self):
        """ Simple Accessor for use by the ComputeResourceAllocator-
        It gives the dictionary of all servers for the purose of resource allocation
        """
        return self.servers
    

class ComputeNodeManagementClient(protocol.Protocol):

    def connectionMade(self):
        print "Connection Made"
        self.buf = []

    def dataReceived(self, data):
        print data

    def connectionLost(self, reason):
        print "Connection Closed"

class ComputeNodeManagementClientFactory(protocol.ClientFactory):

    protocol = ComputeNodeManagementClient

    def clientConnectionFailed(self, _, reason):
        pass

    def gotData(self, data):
        print data
    
