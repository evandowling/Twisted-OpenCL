
class ResourceAllocator(object):
    def __init__(self):
        self.active_simulations = {}
        
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