__author__= "barun"
__date__  = "$20 May, 2011 12:25:36 PM$"


from itertools import izip
from metrics import Metrics
from common_fields import *
#from wireless_fields import *


DATA_PKTS = ('tcp', 'udp', 'ack', 'cbr')
STRICTLY_DATA_PKTS = ('tcp', 'udp',)

def is_control_pkt(pkt_type=''):
    return pkt_type not in DATA_PKTS

# (Rev #35: #4)
# Determine whether the current event is in wired or wireless (new) format
def is_wired(event):
    if len( event ) < 20:    # A rough number
        return True
    else:
        return False
        

#Tokens
S_CUR_NODE_ID_TOKEN = '-Hs'
S_NXT_NODE_ID_TOKEN = '-Hd'
S_TRACE_LEVEL_TOKEN = '-Nl'
S_FLOW_ID_TOKEN     = '-If'
S_SEQ_NUM_TOKEN     = '-Ii'
S_SRC_FIELD_TOKEN   = '-Is'
S_DST_FIELD_TOKEN   = '-Id'
S_PKT_TYPE_TOKEN    = '-It'
S_PKT_LEN_TOKEN     = '-Il'
S_MA_TOKEN          = '-Ma'

# Trace levels -- from where an event has been logged
L_AGENT     = 'AGT'
L_ROUTER    = 'RTR'
L_MAC       = 'MAC'
L_QUEUE     = 'IFQ'

# Field positions
global I_EVENT
global I_TIMESTAMP_TOKEN
global I_TIMESTAMP
global I_CUR_NODE_ID_TOKEN
global I_CUR_NODE_ID
global I_NXT_NODE_ID_TOKEN
global I_NXT_NODE_ID
global I_TRACE_LEVEL_TOKEN
global I_TRACE_LEVEL
global I_SRC_FIELD_TOKEN
global I_SRC_ADDR_PORT
global I_DST_FIELD_TOKEN
global I_DST_ADDR_PORT
global I_PKT_TYPE_TOKEN
global I_PKT_TYPE
global I_PKT_LEN_TOKEN
global I_PKT_LEN
global I_FLOW_ID_TOKEN
global I_FLOW_ID
global I_SEQ_NUM_TOKEN
global I_SEQ_NUM
global I_MA_TOKEN
global I_MA
I_EVENT             = 0
I_TIMESTAMP_TOKEN   = -1
I_TIMESTAMP         = -1
I_CUR_NODE_ID_TOKEN = -1
I_CUR_NODE_ID       = -1
I_NXT_NODE_ID_TOKEN = -1
I_NXT_NODE_ID       = -1
I_TRACE_LEVEL_TOKEN = -1
I_TRACE_LEVEL       = -1
I_SRC_FIELD_TOKEN   = -1
I_SRC_ADDR_PORT     = -1
I_DST_FIELD_TOKEN   = -1
I_DST_ADDR_PORT     = -1
I_PKT_TYPE_TOKEN    = -1
I_PKT_TYPE          = -1
I_PKT_LEN_TOKEN     = -1
I_PKT_LEN           = -1
I_FLOW_ID_TOKEN     = -1
I_FLOW_ID           = -1
I_SEQ_NUM_TOKEN     = -1
I_SEQ_NUM           = -1
I_MA_TOKEN          = -1
I_MA                = -1

# (Rev #35: #4)
# W -- Wired
# WL -- Wireless
global I_W_TIMESTAMP_TOKEN
global I_W_EVENT
global I_W_TIMESTAMP
global I_W_CUR_NODE_ID
global I_W_NXT_NODE_ID
global I_W_PKT_TYPE
global I_W_PKT_LEN
global I_W_PKT_FLAGS
global I_W_FLOW_ID
global I_W_SRC_ADDR_PORT
global I_W_DST_ADDR_PORT
global I_W_SEQ_NUM
global I_W_PKT_ID
global I_WL_EVENT
global I_WL_TIMESTAMP_TOKEN
global I_WL_TIMESTAMP
global I_WL_CUR_NODE_ID_TOKEN
global I_WL_CUR_NODE_ID
global I_WL_NXT_NODE_ID_TOKEN
global I_WL_NXT_NODE_ID
global I_WL_TRACE_LEVEL_TOKEN
global I_WL_TRACE_LEVEL
global I_WL_MA_TOKEN
global I_WL_MA
global I_WL_SRC_FIELD_TOKEN
global I_WL_SRC_ADDR_PORT
global I_WL_DST_FIELD_TOKEN
global I_WL_DST_ADDR_PORT
global I_WL_PKT_TYPE_TOKEN
global I_WL_PKT_TYPE
global I_WL_PKT_LEN_TOKEN
global I_WL_PKT_LEN
global I_WL_FLOW_ID_TOKEN
global I_WL_FLOW_ID
global I_WL_SEQ_NUM_TOKEN
global I_WL_SEQ_NUM
I_W_TIMESTAMP_TOKEN = -1
I_W_EVENT       = -1
I_W_TIMESTAMP   = -1
I_W_CUR_NODE_ID = -1
I_W_NXT_NODE_ID = -1
I_W_PKT_TYPE    = -1
I_W_PKT_LEN     = -1
I_W_PKT_FLAGS   = -1
I_W_FLOW_ID     = -1
I_W_SRC_ADDR_PORT = -1
I_W_DST_ADDR_PORT = -1
I_W_SEQ_NUM     = -1
I_W_PKT_ID      = -1
I_WL_EVENT      = -1
I_WL_TIMESTAMP_TOKEN = -1
I_WL_TIMESTAMP  = -1
I_WL_CUR_NODE_ID_TOKEN = -1
I_WL_CUR_NODE_ID = -1
I_WL_NXT_NODE_ID_TOKEN = -1
I_WL_NXT_NODE_ID = -1
I_WL_TRACE_LEVEL_TOKEN = -1
I_WL_TRACE_LEVEL = -1
I_WL_MA_TOKEN = -1
I_WL_MA = -1
I_WL_SRC_FIELD_TOKEN = -1
I_WL_SRC_ADDR_PORT = -1
I_WL_DST_FIELD_TOKEN = -1
I_WL_DST_ADDR_PORT = -1
I_WL_PKT_TYPE_TOKEN = -1
I_WL_PKT_TYPE   = -1
I_WL_PKT_LEN_TOKEN = -1
I_WL_PKT_LEN    = -1
I_WL_FLOW_ID_TOKEN = -1
I_WL_FLOW_ID    = -1
I_WL_SEQ_NUM_TOKEN = -1
I_WL_SEQ_NUM    = -1


class TraceAnalyzer(object):
    '''
    Trace Analyzer
    '''         

    #
    # A set of filters that can be applied on the list of events    
    #

    ## Get all records pertaining to packet receive event by any node at any level
    #  @param event_list List of events. If not provided, applies fileter on the TraceFile object's events'    
    #  @return A list of receive events    
    def f_receive_events(self, event_list=None):
        if event_list is None:
            event_list = self._all_events       

        list_of_events = [ event for event in event_list if event[I_EVENT] == EVENT_RECEIVE ]

        #print '# of recv events:', len(list_of_events)

        return list_of_events
    
    ## Get all records pertaining to packet receive event for a given node node at any level
    #  @param event_list List of events. If not provided, applies fileter on the TraceFile object's events'
    #  @param node_id Node at which receive event occurs
    #  @return A list of receive events    
    def f_receive_events_at(self, event_list=None, node_id=0):
        if event_list is None:
            event_list = self._all_events       

        assert( I_EVENT == 0 )        
                
        list_of_events = []
        
        if self._sim_mode == MODE_WIRELESS or \
            self._sim_mode == MODE_WIRED:
            list_of_events = [ event for event in event_list if event[I_EVENT] == EVENT_RECEIVE and int(event[I_NXT_NODE_ID]) == int(node_id) ]
        else:
            for event in event_list:
                if event[I_EVENT] == EVENT_RECEIVE:
                    if is_wired(event):
                        if event[I_W_NXT_NODE_ID] == node_id:
                            list_of_events.append(event)
                    else:
                        if event[I_WL_NXT_NODE_ID] == node_id and \
                            event[I_WL_TRACE_LEVEL_TOKEN] == S_TRACE_LEVEL_TOKEN and \
                            event[I_WL_TRACE_LEVEL] == L_AGENT:
                            list_of_events.append(event)
        
        #print '# of recv events:', len(list_of_events)

        return list_of_events


    ## Get all records pertaining to packet send event by any node at any level
    #  @param None
    #  @return A list of send events
    def f_send_events(self, event_list=None):
        if event_list is None:
            event_list = self._all_events
        
        if self._sim_mode == MODE_WIRELESS:
            #print EVENT_SEND
            assert(I_TIMESTAMP_TOKEN == 1)
            list_of_events = [ event for event in event_list if event[I_EVENT] == EVENT_SEND ]
        elif self._sim_mode == MODE_WIRED:
            #print EVENT_DEQUEUE
            list_of_events = [ event for event in event_list if event[I_EVENT] == EVENT_DEQUEUE ]
        else:
            # Mixed mode
            pass

        #print '# of send events:', len(list_of_events)

        return list_of_events


    ## Get all event logged at a given trace level (eg., AGT, MAC, RTR)
    #
    #  <b>Note:</b> This is relevant only for wireless trace files
    #  @param level Layer at which event tracing occured
    #  @return A list events traced at the given layer
    def f_events_at_level(self, event_list=None, level=''):
        if event_list is None: event_list = self._all_events

        # List comprehension is faster compared to iteration over each element
        #
        #   list_of_events = [ event for event in event_list if ... ]
        #
        # ^^^ But the above form may completely fail in non trivial cases, fo example,
        # extracting packet type field from a wireless trace file -- due to non-uniform
        # format

        list_of_events = []
        
        if self._sim_mode == MODE_WIRELESS:
            assert(I_TIMESTAMP_TOKEN == 1)
            if level == '': level = L_AGENT
            #print I_TRACE_LEVEL_TOKEN, S_TRACE_LEVEL_TOKEN
            for event in event_list:
                try:
                    if event[I_TRACE_LEVEL_TOKEN] == S_TRACE_LEVEL_TOKEN and \
                        event[I_TRACE_LEVEL] == level:
                            list_of_events.append(event)
                except IndexError:
                    continue
                            
        #print '# of events at level', level, ':', len(list_of_events)

        return list_of_events

    ## For wireless trace files, there coule be multiple trace levels
    #  For wired, there is no level. So, this method is not applicable for wired
    #  trace files    
    def f_events_at_levels(self, event_list=None, levels=None):
        #print 'Events_at_levels'
        if event_list is None: event_list = self._all_events
        if levels is None: levels = [L_AGENT,]        

        list_of_events = []

        if self._sim_mode == MODE_WIRELESS:
            assert(I_TIMESTAMP_TOKEN == 1)            
            #print I_TRACE_LEVEL_TOKEN, S_TRACE_LEVEL_TOKEN
            for event in event_list:
                try:
                    if event[I_TRACE_LEVEL_TOKEN] == S_TRACE_LEVEL_TOKEN and \
                        event[I_TRACE_LEVEL] in levels:
                            #print event
                            list_of_events.append(event)
                except IndexError:
                    continue

        #print '# of events at levels', levels, ':', len(list_of_events)
        return list_of_events


    ## Get all events logged by a given node
    #  @param node_id ID indicating the node [String]
    #  @return A list events traced for the given node
    def f_events_at_node(self, event_list=None, node_id=0):
        if event_list is None: event_list = self._all_events
        node_id = str(node_id)

        list_of_events = []
        
        if self._sim_mode == MODE_WIRELESS:
            assert(I_TIMESTAMP_TOKEN == 1)
            #print I_TIMESTAMP_TOKEN
            for event in event_list:                
                try:
                    if event[I_CUR_NODE_ID_TOKEN] == S_CUR_NODE_ID_TOKEN and\
                        event[I_CUR_NODE_ID] == node_id:
                            list_of_events.append(event)
                except IndexError:                    
                    continue
        else:
            #print I_TIMESTAMP_TOKEN
            assert(I_TIMESTAMP_TOKEN == -1)
            list_of_events = [ event for event in event_list if event[I_CUR_NODE_ID] == node_id ]

        #print '# of events at node #', node_id, ':', len(list_of_events)
        return list_of_events


    def f_events_with_src_node(self, event_list=None, node_id=0):
        list_of_events = []
        if event_list is None: event_list = self._all_events
        node_id = str(node_id)

        if self._sim_mode == MODE_WIRELESS:
            assert(I_TIMESTAMP_TOKEN == 1)
            for event in event_list:
                try:
                    # split('.')[0] won't work for hierarchical address
                    e_src_add_port = event[I_SRC_ADDR_PORT]
                    if event[I_SRC_FIELD_TOKEN] == S_SRC_FIELD_TOKEN and \
                        e_src_add_port[ :e_src_add_port.rindex('.') ] == node_id:
                        list_of_events.append(event)
                except IndexError:
                    continue
        else:
            assert(I_TIMESTAMP_TOKEN == -1)
            for event in event_list:
                try:
                    e_src_add_port = event[I_SRC_ADDR_PORT]
                    if event[I_SRC_ADDR_PORT][ :e_src_add_port.rindex('.') ] == node_id:
                        list_of_events.append(event)
                except IndexError:
                    continue

        return list_of_events


    def f_events_with_dst_node(self, event_list=None, node_id=0):
        list_of_events = []
        if event_list is None: event_list = self._all_events
        node_id = str(node_id)

        if self._sim_mode == MODE_WIRELESS:
            assert(I_TIMESTAMP_TOKEN == 1)
            for event in event_list:
                try:
                    e_dst_add_port = event[I_DST_ADDR_PORT]
                    if event[I_DST_FIELD_TOKEN] == S_DST_FIELD_TOKEN and \
                        event[I_DST_ADDR_PORT][ :e_dst_add_port.rindex('.') ] == node_id:
                        list_of_events.append(event)
                except IndexError:
                    continue
        else:
            assert(I_TIMESTAMP_TOKEN == -1)
            for event in event_list:
                try:
                    e_dst_add_port = event[I_DST_ADDR_PORT]
                    if event[I_DST_ADDR_PORT][ :e_dst_add_port.rindex('.') ] == node_id:
                        list_of_events.append(event)
                except IndexError:
                    continue

        return list_of_events


    def f_events_with_data_pkts(self, event_list=None):
        if event_list is None: event_list = self._all_events

        list_of_events = []
        if self._sim_mode == MODE_WIRELESS:
            assert(I_TIMESTAMP_TOKEN == 1)
            for event  in event_list:                
                try:
                    if event[I_PKT_TYPE_TOKEN] == S_PKT_TYPE_TOKEN and \
                    event[I_PKT_TYPE] in DATA_PKTS:
                        list_of_events.append(event)
                except IndexError:
                    continue
        elif self._sim_mode == MODE_WIRED:
            assert(I_TIMESTAMP_TOKEN == -1)
            for event in event_list:                
                try:
                    if event[I_PKT_TYPE] in DATA_PKTS:
                        list_of_events.append(event)
                except IndexError:                    
                    continue
        else:
            for event in event_list:  
                if is_wired(event):
                    try:
                        if event[I_W_PKT_TYPE] in DATA_PKTS:
                            list_of_events.append(event)
                    except IndexError:                    
                        continue
                else:
                    try:
                        if event[I_WL_PKT_TYPE] in DATA_PKTS:
                            list_of_events.append(event)
                    except IndexError:                    
                        continue

        #print '# of events with data pkts:', len(list_of_events)
        return list_of_events
    
    
    ## Get a particular column of info (for example, timestamp) for a given set of events
    #  @param events A set of events
    #  @param col_num Column number
    #  @return A list of values for the specified column
    def f_get_cols(self, event_list=None, col_num=0):
        """
        Get a particular column of info (for example, timestamp) for a given set of events
        """
        if event_list is None: event_list = self._all_events

        column = []
        for event in event_list:
            try:
                column.append(event[col_num])
            except IndexError:
                continue

        return column
    

    #
    # Methods to evaluate metrics
    #
    
    def get_average_throughput(self):
        Metrics.average_throughput()


    ## Cumulative sum of bytes received by a node at any given layer -- only for wireless
    #  @param node_id ID of the node
    #  @param levels A list of level name(s)
    #  @return A list in the form [(time_instance, total_bytes),]
    def get_cumulative_bytes_received_for_node_at_layers(self, node_id=0, layers=[]):
        data = []        
        data_set = []
        if layers == []: layers = [L_AGENT,]
            
        #print 'layers:', layers
        
        if self._sim_mode == MODE_WIRELESS or \
            self._sim_mode == MODE_WIRED:
            data = self.f_receive_events_at(self._all_events, node_id)
            #print 'get_cumulative_bytes_received_for_node_at_layers:', len(data)            

            if self._sim_mode == MODE_WIRELESS:                            
                assert(I_TIMESTAMP_TOKEN == 1)
                data = self.f_events_at_levels(data, layers)           
            
            data = self.f_events_with_data_pkts(data)   # All trace types are taken care of
            data_set = izip( self.f_get_cols(data, col_num=I_TIMESTAMP), self.f_get_cols(data, col_num=I_PKT_LEN) )
            #print 'get_cumulative_bytes_received_for_node_at_layers:', len(data)
            
        else:
            # Mixed mode            
            wired_events = []
            wireless_events = []
            rcv_events = self.f_receive_events(self._all_events) # All receive events
            #print 'len(rcv_events):', len(rcv_events)
            
            for e in rcv_events:
                if is_wired(e):
                    if e[I_W_NXT_NODE_ID] == node_id:
                        wired_events.append(e)
                else:
                    if e[I_WL_NXT_NODE_ID] == node_id:
                        wireless_events.append(e)                       
                                        
                    wireless_events = self.f_events_at_levels(wireless_events, layers)              
            
            data = wired_events + wireless_events
            #print 'len(data):', len(data)
            #data = self.f_events_with_data_pkts(data)   # All trace types are taken care of
            c_ts = self.f_get_cols(wired_events, col_num=I_W_TIMESTAMP) + \
                    self.f_get_cols(wireless_events, col_num=I_WL_TIMESTAMP)
            c_len = self.f_get_cols(wired_events, col_num=I_W_PKT_LEN) + \
                    self.f_get_cols(wireless_events, col_num=I_WL_PKT_LEN)                                  
          
            data_set = izip( c_ts, c_len )
            #print c_ts[:10]
            
          
        
        return Metrics.cumulative_bytes_received(data_set)


    def get_cumulative_throughput_for_node(self, node_id=0):
        data = self.f_receive_events_at(self._all_events, node_id)
        #data = self.f_events_at_node(data, node_id)

        if self._sim_mode == MODE_WIRELESS:
            assert(I_TIMESTAMP_TOKEN == 1)
            data = self.f_events_at_level(data, 'AGT')

        data = self.f_events_with_data_pkts(data)

        data_set = []
        data_set = izip( self.f_get_cols(data, col_num=I_TIMESTAMP), self.f_get_cols(data, col_num=I_PKT_LEN) )
        #for e in data_set: print e

        return Metrics.cumulative_throughput(data_set)
    

    def get_instantaneous_throughput_for_node(self, node_id=0):
        data = self.f_receive_events_at(self._all_events, node_id)
        #data = self.f_events_at_node(data, node_id)

        if self._sim_mode == MODE_WIRELESS:
            assert(I_TIMESTAMP_TOKEN == 1)
            data = self.f_events_at_level(data, 'AGT')

        data = self.f_events_with_data_pkts(data)

        data_set = []
        data_set = izip( self.f_get_cols(data, col_num=I_TIMESTAMP), self.f_get_cols(data, col_num=I_PKT_LEN) )
        #for e in data_set: print e
        
        return Metrics.instantaneous_throughput(data_set)


    def get_average_throughput_for_node(self, node_id=0):
        data_set = []       
        data = self.f_receive_events_at(self._all_events, node_id)

        if self._sim_mode == MODE_WIRELESS:
            assert(I_TIMESTAMP_TOKEN == 1)
            data = self.f_events_at_level(data, 'MAC')

        data = self.f_events_with_data_pkts(data)
        
        if self._sim_mode == MODE_WIRELESS or \
            self._sim_mode == MODE_WIRED:
            data_set = izip( self.f_get_cols(data, col_num=I_TIMESTAMP), self.f_get_cols(data, col_num=I_PKT_LEN) )
        else:
            c_ts = []
            c_len = []
            for e in data:
                #print e
                if is_wired(e):
                    c_ts.append( e[I_W_TIMESTAMP] )
                    c_len.append( e[I_W_PKT_LEN] )
                else:
                    c_ts.append( e[I_WL_TIMESTAMP] )
                    c_len.append( e[I_WL_PKT_LEN] )
                    
            data_set = izip(c_ts, c_len)
       
        #for e in data_set: print e        
        return Metrics.average_throughput( data_set, -1 )


    ## Compute the end to end delay of packet transmissions between two nodes
    #
    #  <b>Note:</b> This doesn't work for CBR traffic
    #  @param src_node ID of the node sending packets
    #  @param dst_node ID of the node receiving packets
    #  @return A list in the format [(pkt_seq_num, delay)]
    def get_end2end_delay(self, src_node=0, dst_node=0):
        data = self.f_send_events(self._all_events)
        data = self.f_events_at_node(data, src_node)
        
        if self._sim_mode == MODE_WIRELESS:
            assert(I_TIMESTAMP_TOKEN == 1)
            data = self.f_events_at_level(data, L_AGENT)

        data = self.f_events_with_data_pkts(data)
        
        pkt_seq_num = []
        pkt_timestamp = []
        #print data[:10]

        if self._sim_mode == MODE_WIRELESS:
            assert(I_TIMESTAMP_TOKEN == 1)
            for event in data:
                try:
                    if event[I_SEQ_NUM_TOKEN] == S_SEQ_NUM_TOKEN:   # Wireless, from AGT
                        pkt_seq_num.append( event[I_SEQ_NUM] )
                        pkt_timestamp.append( event[I_TIMESTAMP] )
                except IndexError:
                    continue
        else:
            assert(I_TIMESTAMP_TOKEN == -1)
            for event in data:
                try:                    
                    pkt_seq_num.append( event[I_SEQ_NUM] )
                    pkt_timestamp.append( event[I_TIMESTAMP] )
                except IndexError:
                    continue

        
        send_pkts = izip( pkt_seq_num, pkt_timestamp )
        
        data = self.__common_filters__(dst_node)
        pkt_seq_num = []
        pkt_timestamp = []
        
        #print data[:10]
        if self._sim_mode == MODE_WIRELESS:
            for event in data:
                try:
                    if event[I_SEQ_NUM_TOKEN] == S_SEQ_NUM_TOKEN:   # Wireless, from AGT
                        pkt_seq_num.append( event[I_SEQ_NUM] )
                        pkt_timestamp.append( event[I_TIMESTAMP] )
                except IndexError:
                    continue
        else:
            for event in data:
                try:
                    pkt_seq_num.append( event[I_SEQ_NUM] )
                    pkt_timestamp.append( event[I_TIMESTAMP] )
                except IndexError:
                    continue
        
        rcvd_pkts = izip( pkt_seq_num, pkt_timestamp )

        return Metrics.end2end_delay(send_pkts, rcvd_pkts)


    ## Get the # of packet retransmissions, if any, between two given nodes
    #  @param src_node ID of the node sending packets
    #  @param dst_node ID of the node receiving packets
    #  @return A list in the format [(pkt_seq_num, retransmission_count)]
    def get_packet_retransmissions(self, src_node=0, dst_node=0):
        data = self.f_send_events(self._all_events)
        data = self.f_events_at_node(data, src_node)

        if self._sim_mode == MODE_WIRELESS:
            assert(I_TIMESTAMP_TOKEN == 1)
            data = self.f_events_at_level(data, L_AGENT)
            
        data = self.f_events_with_data_pkts(data)
        
        # Check for destination node
        data = self.f_events_with_dst_node(data, dst_node)
                
        pkt_seq_num = []
        if self._sim_mode == MODE_WIRELESS:
            for event in data:
                try:
                    if event[I_SEQ_NUM_TOKEN] == S_SEQ_NUM_TOKEN:   # Wireless, from AGT
                        pkt_seq_num.append( event[I_SEQ_NUM] )
                except IndexError:
                    continue
        elif self._sim_mode == MODE_WIRED:
            assert(I_TIMESTAMP_TOKEN == -1)
            for event in data:
                try:
                    pkt_seq_num.append( event[I_SEQ_NUM] )
                except IndexError:
                    continue

        #pkt_seq_num = self.f_get_cols(data, col_num=I_SEQ_NUM)
        #print pkt_seq_num[:40]
        return Metrics.packet_retransmissions(pkt_seq_num)


    # (Rev #28 : #3)
    ## Cumulative sum of bytes received by a node until it receives the last packet
    #  @param src_node ID of the source node
    #  @param src_port Port # of the source node
    #  @param dst_node ID of the destination node
    #  @param dst_port Port# of the destination node
    #  @return A list in the form [(pkt #, hop_count),]
    def get_hop_count_pkt_seq_num(self, src_node=0, src_port=0, dst_node=0, dst_port=0):
        # TODO: Fix for wireless
        cur_seq_num = 0
        hop_count = 0
        result = []
        counter = {}
        n = 0
        #print 'Length', len(self._all_events)
        
        for event in self._all_events:                                 
            
            try:
                assert(I_SEQ_NUM > 0)
                event_type = event[I_EVENT]
                try:
                    event_seq_num = int(event[I_SEQ_NUM]) 
                    # split('.')[0] won't work for hierarchical address
                    #event_src_id, event_src_port = [ int(k) for k in event[I_SRC_ADDR_PORT].split('.') ]
                    #event_dst_id, event_dst_port = [ int(k) for k in event[I_DST_ADDR_PORT].split('.') ]
                    e_src_add_port  = event[I_SRC_ADDR_PORT]
                    e_dst_add_port  = event[I_DST_ADDR_PORT]
                    event_src_id    = int( e_src_add_port[ :e_src_add_port.rindex('.') ] )
                    event_src_port  = int( e_src_add_port[ e_src_add_port.rindex('.')+1: ] )
                    event_dst_id    = int( e_dst_add_port[ :e_dst_add_port.rindex('.') ] )
                    event_dst_port  = int( e_dst_add_port[ e_dst_add_port.rindex('.')+1: ] )
                    #print 'Hop count:', event_src_id, ':', event_src_port, event_dst_id, ':', event_dst_port
                    #print event[I_SEQ_NUM], event_seq_num, event_src_id, event_src_port, event_dst_id, event_dst_port, event[21], event[22]
                    
                    assert(event_seq_num >= 0)                               
                    #print event_type
                    if event_type in ('-', 's'):    # Pkt send in wired & wireless trace files
                        # We only need to count pkt send events                

                        if event_src_id == src_node and event_src_port == src_port\
                            and event_dst_id == dst_node and event_dst_port == dst_port:
                                #print result  
                                try:
                                    if self._sim_mode == MODE_WIRED or \
                                        ( self._sim_mode == MODE_WIRELESS \
                                         and event[I_SEQ_NUM_TOKEN] == S_SEQ_NUM_TOKEN \
                                         and event[I_NXT_NODE_ID_TOKEN] == S_NXT_NODE_ID_TOKEN \
                                         and event[I_TRACE_LEVEL] == L_MAC \
                                         and int(event[I_NXT_NODE_ID]) != int(event_src_id) ):                                            
                                            # For wireless, ignore broadcasts
                                            # Also, at times, the pkt comes back to the sender -- 
                                            # dont' know why                                           
                                            
                                            #print event[I_NXT_NODE_ID], event_src_id, event_src_id != event[I_NXT_NODE_ID]                                                
                                            try:                                                   
                                                counter[event_seq_num] += 1
                                                #print 'Increment for', event_seq_num
                                            except KeyError:
                                                counter[event_seq_num] = 1
                                                    
                                except IndexError:
                                    continue 
                    
                except ValueError:
                    #print 'ValueError'
                    continue                           
                                
            except IndexError:
                continue                                                                                    
        
        for key, val in counter.items():
            result.append( (key, val,) )
            
        result.sort()
        #print result[:20]
        return result
    

    def __common_filters__(self, node_id=0, trace_level=L_AGENT):
        data = self.f_receive_events_at(self._all_events, node_id)
        #print 'common_filters:', data[:15]
        #print ''
        #data = self.f_events_at_node(data, node_id)
        #print 'common_filters:', data[:15]
        if self._sim_mode == MODE_WIRELESS:
            assert(I_TIMESTAMP_TOKEN == 1)
            data = self.f_events_at_level(data, trace_level)
        data = self.f_events_with_data_pkts(data)
        
        return data
    
           
    #
    # Simulation model related methods
    #

    ## Return the time duration for which the simulation ran
    def get_simulation_time(self):        
        stop = 0

        # Typically we could just check for the first event, but
        # We need to scan the events because there could be logs for mobility or something else...        
        if self._sim_mode == MODE_WIRELESS or \
            self._sim_mode == MODE_WIRED:
            # Scan records from the end
            for record in self._all_events[::-1]:
                #print record
                if record[I_EVENT] in NS_EVENTS:
                    stop = float(record[I_TIMESTAMP])
                    #print 'stop:', stop
                    break
        else:            
            for record in self._all_events[::-1]:
                if record[I_EVENT] in NS_EVENTS:                    
                    if is_wired( record ):                        
                        stop = float(record[I_W_TIMESTAMP])                        
                        break
                    else:                        
                        stop = float(record[I_WL_TIMESTAMP])                        
                        break
               
        return stop
    
    
    ## Determine the time at which traffic exchange started
    def get_traffic_start_time(self):
        # Identify first send event
        # Identify last receive event -- or simulation end???
        first_send_time = 0
        if self._sim_mode == MODE_WIRELESS or \
            self._sim_mode == MODE_WIRED:
                for event in self._all_events:
                    if event[I_EVENT] == EVENT_DEQUEUE or \
                        event[I_EVENT] == EVENT_SEND:
                            first_send_time = float(event[I_TIMESTAMP])
                            break
        else:            
            for record in self._all_events:
                if record[I_EVENT] in NS_EVENTS:                    
                    if is_wired( record ):                        
                        first_send_time = float(record[I_W_TIMESTAMP])                        
                        break
                    else:                        
                        first_send_time = float(record[I_WL_TIMESTAMP])                        
                        break
                            
        return first_send_time
    

    def get_first_receive_time(self):
        first_recv_time = 0
        
        # Events are always at 1st col
        for event in self._all_events:
            if event[I_EVENT] == EVENT_RECEIVE:
                if self._sim_mode == MODE_WIRELESS or \
                    self._sim_mode == MODE_WIRED:
                    first_recv_time = float(event[I_TIMESTAMP])
                else:
                    if is_wired(event):
                        first_recv_time = float(event[I_W_TIMESTAMP])
                    else:
                        first_recv_time = float(event[I_WL_TIMESTAMP])
                break       
                            
        return first_recv_time
    
    
    def get_last_receive_time(self):
        last_recv_time = 0
        
        # Events are always at 1st col
        for event in self._all_events[::-1] :   # Read the list backwards
            if event[I_EVENT] == EVENT_RECEIVE:
                if self._sim_mode == MODE_WIRELESS or \
                    self._sim_mode == MODE_WIRED:
                    last_recv_time = float(event[I_TIMESTAMP])
                else:
                    if is_wired(event):
                        last_recv_time = float(event[I_W_TIMESTAMP])
                    else:
                        last_recv_time = float(event[I_WL_TIMESTAMP])
                break
                            
        return last_recv_time
    
        
    def get_statistics(self):
        #print 'Stats'        
        duration = self.get_simulation_time()
        msg = '''
        Simulation duration: %f     
        ''' % duration
        #print msg
        return msg


    ## Create a TraceAnalyzer object, and store all the events into it
    #  @param self Points to current object
    #  @param file_name Path of the trace file to be analyzed
    def __init__(self, file_name=None, mode=MODE_WIRELESS):
        #print 'Creating TraceAnalyzer object from %s ...' % file_name
        self._all_events = []
        
        try:
            trace_file = open(file_name, 'r')
            for event in trace_file:
		if event:
                	#self._all_events.append(event.split())
                	self._all_events.append((event or '').split())
        except IOError, ioe:
            #print 'IOError:', str(ioe)
            return None #HttpResponse(str(ioe))

        ### How to detect the mode ???
        self._sim_mode = mode
        #print 'Trace file mode:', self._sim_mode

        global I_EVENT
        global I_TIMESTAMP_TOKEN
        global I_TIMESTAMP
        global I_CUR_NODE_ID_TOKEN
        global I_CUR_NODE_ID
        global I_NXT_NODE_ID_TOKEN
        global I_NXT_NODE_ID
        global I_TRACE_LEVEL_TOKEN
        global I_TRACE_LEVEL
        global I_SRC_FIELD_TOKEN
        global I_SRC_ADDR_PORT
        global I_DST_FIELD_TOKEN
        global I_DST_ADDR_PORT
        global I_PKT_TYPE_TOKEN
        global I_PKT_TYPE
        global I_PKT_LEN_TOKEN
        global I_PKT_LEN
        global I_FLOW_ID_TOKEN
        global I_FLOW_ID
        global I_SEQ_NUM_TOKEN
        global I_SEQ_NUM
        global NS_EVENTS
        global I_MA_TOKEN
        global I_MA
        # Mixed
        global I_W_TIMESTAMP_TOKEN
        global I_W_EVENT
        global I_W_TIMESTAMP
        global I_W_CUR_NODE_ID
        global I_W_NXT_NODE_ID
        global I_W_PKT_TYPE
        global I_W_PKT_LEN
        global I_W_PKT_FLAGS
        global I_W_FLOW_ID
        global I_W_SRC_ADDR_PORT
        global I_W_DST_ADDR_PORT
        global I_W_SEQ_NUM
        global I_W_PKT_ID
        global I_WL_EVENT
        global I_WL_TIMESTAMP_TOKEN
        global I_WL_TIMESTAMP
        global I_WL_CUR_NODE_ID_TOKEN
        global I_WL_CUR_NODE_ID
        global I_WL_NXT_NODE_ID_TOKEN
        global I_WL_NXT_NODE_ID
        global I_WL_TRACE_LEVEL_TOKEN
        global I_WL_TRACE_LEVEL
        global I_WL_MA_TOKEN
        global I_WL_MA
        global I_WL_SRC_FIELD_TOKEN
        global I_WL_SRC_ADDR_PORT
        global I_WL_DST_FIELD_TOKEN
        global I_WL_DST_ADDR_PORT
        global I_WL_PKT_TYPE_TOKEN
        global I_WL_PKT_TYPE
        global I_WL_PKT_LEN_TOKEN
        global I_WL_PKT_LEN
        global I_WL_FLOW_ID_TOKEN
        global I_WL_FLOW_ID
        global I_WL_SEQ_NUM_TOKEN
        global I_WL_SEQ_NUM

        if self._sim_mode == MODE_WIRELESS:            
            #print 'Wireless mode'
            # Field positions
            I_EVENT             = 0
            I_TIMESTAMP_TOKEN   = 1
            I_TIMESTAMP         = 2
            I_CUR_NODE_ID_TOKEN = 3
            I_CUR_NODE_ID       = 4
            I_NXT_NODE_ID_TOKEN = 5
            I_NXT_NODE_ID       = 6
            I_TRACE_LEVEL_TOKEN = 17
            I_TRACE_LEVEL       = 18
            I_MA_TOKEN          = 21
            I_MA                = 22
            I_SRC_FIELD_TOKEN   = 29
            I_SRC_ADDR_PORT     = 30    # Combined together: addr.port
            I_DST_FIELD_TOKEN   = 31
            I_DST_ADDR_PORT     = 32    # Combined together: addr.port
            I_PKT_TYPE_TOKEN    = 33
            I_PKT_TYPE          = 34
            I_PKT_LEN_TOKEN     = 35
            I_PKT_LEN           = 36
            I_FLOW_ID_TOKEN     = 37
            I_FLOW_ID           = 38
            I_SEQ_NUM_TOKEN     = 39
            I_SEQ_NUM           = 40
            NS_EVENTS = (EVENT_SEND, EVENT_RECEIVE, EVENT_DROP, EVENT_FORWARD, )
            
        elif self._sim_mode == MODE_WIRED:            
            #print 'Wired mode'
            # Field positions            
            I_TIMESTAMP_TOKEN   = -1
            I_EVENT             = 0            
            I_TIMESTAMP         = 1
            I_CUR_NODE_ID       = 2
            I_NXT_NODE_ID       = 3
            I_PKT_TYPE          = 4
            I_PKT_LEN           = 5
            I_PKT_FLAGS         = 6
            I_FLOW_ID           = 7
            I_SRC_ADDR_PORT     = 8    # Combined together: addr.port
            I_DST_ADDR_PORT     = 9    # Combined together: addr.port
            I_SEQ_NUM           = 10
            I_PKT_ID            = 11
            NS_EVENTS = (EVENT_RECEIVE, EVENT_DROP, EVENT_ENQUEUE, EVENT_DEQUEUE, )
            
        else:
            # We gotta know about all kinda fields!
            # print 'Mixed mode'
            I_W_TIMESTAMP_TOKEN   = -1
            I_W_EVENT             = 0            
            I_W_TIMESTAMP         = 1
            I_W_CUR_NODE_ID       = 2
            I_W_NXT_NODE_ID       = 3
            I_W_PKT_TYPE          = 4
            I_W_PKT_LEN           = 5
            I_W_PKT_FLAGS         = 6
            I_W_FLOW_ID           = 7
            I_W_SRC_ADDR_PORT     = 8    # Combined together: addr.port
            I_W_DST_ADDR_PORT     = 9    # Combined together: addr.port
            I_W_SEQ_NUM           = 10
            I_W_PKT_ID            = 11
            # Wireless
            I_WL_EVENT             = 0
            I_WL_TIMESTAMP_TOKEN   = 1
            I_WL_TIMESTAMP         = 2
            I_WL_CUR_NODE_ID_TOKEN = 3
            I_WL_CUR_NODE_ID       = 4
            I_WL_NXT_NODE_ID_TOKEN = 5
            I_WL_NXT_NODE_ID       = 6
            I_WL_TRACE_LEVEL_TOKEN = 17
            I_WL_TRACE_LEVEL       = 18
            I_WL_MA_TOKEN          = 21
            I_WL_MA                = 22
            I_WL_SRC_FIELD_TOKEN   = 29
            I_WL_SRC_ADDR_PORT     = 30    # Combined together: addr.port
            I_WL_DST_FIELD_TOKEN   = 31
            I_WL_DST_ADDR_PORT     = 32    # Combined together: addr.port
            I_WL_PKT_TYPE_TOKEN    = 33
            I_WL_PKT_TYPE          = 34
            I_WL_PKT_LEN_TOKEN     = 35
            I_WL_PKT_LEN           = 36
            I_WL_FLOW_ID_TOKEN     = 37
            I_WL_FLOW_ID           = 38
            I_WL_SEQ_NUM_TOKEN     = 39
            I_WL_SEQ_NUM           = 40
            
            NS_EVENTS = (EVENT_SEND, EVENT_RECEIVE, EVENT_DROP, EVENT_FORWARD, EVENT_ENQUEUE, EVENT_DEQUEUE, )
