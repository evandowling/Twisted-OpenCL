from compute_node_management.compute_node_management import *
from compute_node_transport.compute_node_transport import *
from simulation_allocation.resource_allocator import *


class Postman(object):
    def __init__(self):
        self.resource_allocator = ResourceAllocator(self)
        self.compute_node_management_factory = ComputeNodeManagementFactory(self)
        self.simulation_transport = ComputeNodeTransportClientFactory(self)
        self.simulations = {}
        
    def sendData(self,data):
        """
        Route data to the simulation nodes
        """
        print data
        
    def queueSimulation(self,simulation_struct):
        """
        Start up a simulation with the right seed data
        """
        
    def notifyServerDown(self,servers,server_id):
        """
        Perform the necessary actions to recover from a network failure
        """
        self.resource_allocator.notifyServerDown(servers,server_id)
    
    def __del__(self):
        del self.resource_allocator
        del self.compute_node_management_factory
        del self.simulation_transport
        for sim_id in self.simulations.items():
            del self.simulations[sim_id]
            
if __name__ == '__main__':
    p = Postman()
    reactor.run()