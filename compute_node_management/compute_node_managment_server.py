from twisted.internet import reactor
from compute_node_management import *

reactor.connectTCP('127.0.0.1', 6666, ComputeNodeManagementClientFactory())
reactor.run()