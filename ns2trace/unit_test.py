import unittest
import time
#from trace_analyzer_old import TraceAnalyzer
from trace_analyzer import TraceAnalyzer
from metrics import Metrics
from common_fields import *


class  UnitTestCase(unittest.TestCase):
    #def setUp(self):
    #    self.foo = Unit_()
    #

    #def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None

    def test_unit_1_(self):
#        assert x != y;
#        self.assertEqual(x, y, "Msg");
#        self.fail("TODO: Write test")

        print ''
        print 'Test case #1: Wireless mode'
        start = time.time()
        ta = TraceAnalyzer('/home/barun/codes/ns2/exp7/dsr-6-nodes.tr')       
        print ta.get_average_throughput_for_node(5)
        print ta.get_instantaneous_throughput_for_node(5)
        print ta.get_cumulative_throughput_for_node(5)
        print ta.get_cumulative_bytes_received_for_node(5)
        print ta.get_end2end_delay(0, 5)
        print ta.get_packet_retransmissions(0, 5)
        end = time.time()
        print 'Time consumed:', end - start

        
    def test_unit_2_(self):
        print ''
        print 'Test case #2: Wired mode'
        start = time.time()
        ta = TraceAnalyzer('/home/barun/codes/ns2/my_trace_analyzer/wired_error.tr', mode=MODE_WIRED)        
        print ta.get_average_throughput_for_node(2)
        print ta.get_instantaneous_throughput_for_node(2)
        print ta.get_cumulative_throughput_for_node(2)
        print ta.get_cumulative_bytes_received_for_node(2)
        print ta.get_end2end_delay(0, 2)
        print ta.get_packet_retransmissions(0, 2)
        end = time.time()
        print 'Time consumed:', end - start

if __name__ == '__main__':
    unittest.main()

