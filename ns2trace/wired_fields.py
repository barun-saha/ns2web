__author__= "barun"
__date__  = "$20 May, 2011 12:18:25 PM$"

# Different events and their symbolic representations in a trace file
EVENT_DROP = 'd'
EVENT_RECEIVE = 'r'
EVENT_ENQUEUE = '+'
EVENT_DEQUEUE = '-'

NS_EVENT_TYPE = {
    EVENT_DROP: 'Drop',
    EVENT_RECEIVE: 'Receive',
    EVENT_ENQUEUE: 'Enqueue',
    EVENT_DEQUEUE: 'Dequeue',
}

# Field positions
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