__author__= "barun"
__date__  = "$21 May, 2011 11:03:04 PM$"


# Simulation modes
MODE_WIRED  = 'Wired'
MODE_WIRELESS   = 'Wireless'
MODE_SATELLITE  = 'Satellite'
MODE_MIXED  = 'Mixed'

SIMULATION_MODES   = (MODE_WIRED, MODE_WIRELESS, MODE_SATELLITE, MODE_MIXED,)

# Simulation events
EVENT_SEND      = 's'   # Wireless
EVENT_RECEIVE   = 'r'   # Wireless, wired
EVENT_DROP      = 'd'   # Wireless, wired
EVENT_FORWARD   = 'f'   # Wireless
EVENT_ENQUEUE   = '+'   # Wired
EVENT_DEQUEUE   = '-'   # Wired

NS_EVENT_TYPE = {
    EVENT_SEND:     'Send',
    EVENT_RECEIVE:  'Receive',
    EVENT_DROP:     'Drop',
    EVENT_FORWARD:  'Forward',
    EVENT_ENQUEUE:  'Enqueue',
    EVENT_DEQUEUE:  'Dequeue',
}