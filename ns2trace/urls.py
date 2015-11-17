# Ns2Trace

__author__= "barun"
__date__  = "$24 May, 2011 5:04:01 PM$"


from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import *


urlpatterns = patterns('ns2web.ns2trace.web_views',
    url(r'^(?P<sim_mode>[a-zA-Z]+?)/$',             'initialize',),
    url(r'^general_stats/$',                        'general_stats', ),
    url(r'^avg_thruput/(?P<node_id>\d+)/$',           'avg_thruput',),
    # (Rev #32: #3)
    # When no trace level is specified
    url(r'^plot/bytes_rcvd/(?P<node_id>\d+)/(?P<levels>X)/$',            'bytes_received_at_levels',),
    url(r'^plot/bytes_rcvd/(?P<node_id>\d+)/(?P<levels>([a-zA-Z]{3}[|]{1})*)/$',            'bytes_received_at_levels',),
    # (Rev #28: #4)
    #url(r'^plot/end2end_delay/(?P<src_node>\d+)/(?P<dst_node>\d+)/$',      'end2end_delay',),
    # http://stackoverflow.com/questions/4703390/how-to-extract-a-floating-number-from-a-string-in-python/4703409#4703409
    url(r'^plot/end2end_delay/(?P<src_node>\d+)/(?P<dst_node>\d+)/(?P<scale>[-+]?\d*\.\d+|\d+)/$',      'end2end_delay',),
    url(r'^plot/pkt_retransmits/(?P<src_node>\d+)/(?P<dst_node>\d+)/$',    'pkt_retransmits',),
    url(r'^clear_session/$',                        'clear_session',),
    # (Rev #28 : #3)
    url(r'^plot/hop_cnt_seq_num/(?P<src_node>\d+)/(?P<src_port>\d+)/(?P<dst_node>\d+)/(?P<dst_port>\d+)/$',    
        'hop_count_pkt_seq_num',),
)
