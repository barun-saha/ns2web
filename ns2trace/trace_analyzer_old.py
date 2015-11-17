__author__= "barun"
__date__  = "$20 May, 2011 12:25:36 PM$"

from metrics import Metrics
from wireless_fields import *


DATA_PKTS = ('tcp', 'udp', 'ack',)
def is_control_pkt(pkt_type=''):
    return pkt_type not in DATA_PKTS


class TraceAnalyzer(object):
    '''
    Trace Analyzer
    '''

    def __init__(self, file_name=None):
        print 'Trace Analyzer'        
        
        self._receiveEvents = []
        self._sendEvents = []
        self._dropEvents = []
        self._otherEvents = []

        self._data_pkts_rcvd = []
        self._cntrl_pkts_rcvd = []

        self._sourceNodes = []
        self._destinationNodes = []

        self.parse_events(file_name)
        self.get_statistics()
        

    def parse_events(self, file_name):
        '''
        Parse the send, receive and drop events, and store them in a list. This
        method should get called only once (from inside __init__) at the
        beginning of processing.
        '''
        print 'Parse events -- Use normal record scan to filter receive events'
        if file_name:
            trace_file = None
            try:
                trace_file = open(file_name, 'r')
                
                for event in trace_file:
                    if event[0] == EVENT_RECEIVE:
                        self._receiveEvents.append(event)                                               
                    elif event[0] == EVENT_SEND:
                        self._sendEvents.append(event)
                    elif event[0] == EVENT_DROP:
                        self._dropEvents.append(event)
                    else:
                        self._otherEvents.append(event)
            except IOError, ioe:
                print 'IOError:', str(ioe)
            finally:
                if trace_file:
                    trace_file.close()

            for event in self._receiveEvents:
                event = event.split()
                try:
                    if event[I_PKT_TYPE_TOKEN] == S_PKT_TYPE_TOKEN and\
                        event[I_TRACE_LEVEL_TOKEN] == S_TRACE_LEVEL_TOKEN and\
                        event[I_PKT_TYPE] in DATA_PKTS:
                            self._data_pkts_rcvd.append(event)
                    else:
                            self._cntrl_pkts_rcvd.append(event)
                except IndexError:
                    #print event
                    self._data_pkts_rcvd.append(event)
                    continue

            # Determine sending and receiving nodes
            for event in self._sendEvents:
                try:
                    event = event.split()
                    if event[I_PKT_TYPE_TOKEN] == S_PKT_TYPE_TOKEN and \
                    event[I_PKT_TYPE] in DATA_PKTS:
                        if event[I_SRC_FIELD_TOKEN] == S_SRC_FIELD_TOKEN:
                            src = event[I_SRC_ADDR_PORT].split('.')[0]
                            if src not in self._sourceNodes and int(src) >= 0:
                                self._sourceNodes.append(src)
                    else:
                        continue

#       Is is required to have destination nodes???
#       In case of TCP, source nodes themselves will become
#       destination of acknowledgements
#
#                        if event[I_PKT_TYPE_TOKEN] == S_PKT_TYPE_TOKEN and \
#                        event[I_PKT_TYPE] in DATA_PKTS:
#                            if event[I_DST_FIELD_TOKEN] == S_DST_FIELD_TOKEN:
#                                dst = event[I_DST_ADDR_PORT].split('.')[0]
#                                if dst not in self._destinationNodes and int(dst) >= 0:
#                                    self._destinationNodes.append(dst)
#                        else:
#                            continue
                except IndexError:
                    # IndexError can occur because certain log entries from MAC
                    # layer may not have source and destination infos -- don't
                    # know exactly why
                    continue

            # Compute simulation times
            try:
                self._simulationStartTime = float(self._sendEvents[0].split()[I_TIMESTAMP])
            except IndexError:
                self._simulationStartTime = 0

            try:
                self._simulationEndTime = float(self._sendEvents[len(self._sendEvents)-1].split()[I_TIMESTAMP])
            except IndexError:
                self._simulationEndTime = 0

            self._simulationDuration = self._simulationEndTime - self._simulationStartTime

            


    def get_statistics(self):
        msg = '''
        Simulation start: %f
        Simulation end: %f
        Duration: %f
        Source nodes: %s        
        # of packets sent: %d
        # of packets received:  %d
           # of data packets:   %d
           # of control packets:%d
        # of packets droped: %d
        # of other events: %d
        ''' % (
            self._simulationStartTime,
            self._simulationEndTime,
            self._simulationDuration,
            self._sourceNodes,            
            len(self._sendEvents),
            len(self._receiveEvents),
            len(self._data_pkts_rcvd),
            len(self._cntrl_pkts_rcvd),
            len(self._dropEvents),
            len(self._otherEvents),
        )
        print msg
        
    def get_average_throughput(self):
        Metrics.averageThroughput()

    def get_instantaneous_throughput(self):
        Metrics.instantaneousThroughput()

