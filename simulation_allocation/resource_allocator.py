
class ResourceAllocator(object):
    def __init__(self, simulation_manager):
        self.simulation_manager = simulation_manager
        self.pending_simulations = {}
        
    def notifyServerDown(self,servers,server_id):
        """
        Perform the necessary actions to recover from a network failure
        """
        
    def setTransform(self,transform_packet):
        """ 
        Call the transform parser to get OpenCL code, set that code as the eval target 
        """
        
    def setInitialConditions(self,data_packet):
        """ 
        Call the data parser to get OpenCL data nodes, insert this data into the data structure
        """
    
    def performComputation(self,simulation_id):
        """
        Signal the system to begin the simulation as soon as the requisite resources are acquired
        """
        if self.pending_simulations[simulation_id]:
            self.simulation_manager.queueSimulation(self.pending_simulations[simulation_id])
            del self.pending_simulations[simulation_id]
        
        