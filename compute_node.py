import sys
from compute_node_management.compute_node_management import *
from compute_node_transport.compute_node_transport import *

class ComputeNode(object):
    def __init__(self):
        """
        Set up the reactor stuff
        """
        self.transport_client = ComputeNodeTransportClientFactory(self)
        self.management_client = ComputeNodeManagementClientFactory()
    
    def start_services(self,transport_port,management_port,postman_ip):
        reactor.connectTCP(postman_ip, transport_port,self.transport_client)
        reactor.connectTCP(postman_ip, management_port,self.management_client)
        
        
if __name__ == '__main__':
    transport = int(sys.argv[1])
    management = int(sys.argv[2])
    postman_ip = sys.argv[3]

    cn = ComputeNode()
    cn.start_services(transport,management,postman_ip)
    reactor.run()