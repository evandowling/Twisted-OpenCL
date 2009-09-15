

class ComputeCore(object):
    def __init__(self):
        """ 
        We will initialize all of the libraries here, and set up the plugin DSL.
        Basically we want to be able to translate our web language into OpenCL here
        """
        
    def setTransform(self,transform_packet):
        """ 
        Call the transform parser to get OpenCL code, set that code as the eval target 
        """
        
    def setData(self,data_packet):
        """ 
        Call the data parser to get OpenCL data nodes, insert this data into the data structure
        """
        
    def performTransform(self):
        """ 
        Perform the previously set transform on the specified data,
        return a data packet to be transmitted back to the postman service
        """
        return "DAT[]end;;"
    
    def lostManager(self,remote):
        """ 
        Free resources tied up by the lost remote manager if any,
        ultimately this might be used to allow compute cores to be managed by multiple processes
        which will be useful if network overhead has them idle for decent amounts of time
        """