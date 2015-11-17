# Ns2Trace

__author__= "barun"
__date__  = "$24 May, 2011 5:00:13 PM$"


from django.http import HttpRequest
from django.core.context_processors import request
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext

from ns2web.ns2trace.trace_analyzer import TraceAnalyzer
import common_fields as cf

from django.conf import settings
from django.template.loader import render_to_string
import subprocess as sp
import os
import re
import json


NS_TRACEFILE_KEY    = 'trace_file_name'    # Key to store trace file name in seesion
NS_TRACEFILE_MODE   = 'trace_file_mode'
#TRACE_ANALYZER_KEY  = 'ta_object'        # Key to store TraceAnalyzer object

INVALID_SESSION_MSG = 'Invalid session! Please start with running the simulation again.'


def initialize(request, sim_mode=''):
    #print 'Initializing ...'
    # Trace file name (physical path) can be found from this
    #request.session[request.session.session_key] = {'trace_file_name' : trace_file_name}
    #
    try:
        d = request.session.get(request.session.session_key)
        #print d
        if d is None:
            raise Exception, INVALID_SESSION_MSG
        if NS_TRACEFILE_KEY in d:
            #print 'Trace file key found'

            # Set the simulation mode
            d[NS_TRACEFILE_MODE] = sim_mode
            request.session[request.session.session_key] = d
            #print 'Trace file format set to:', sim_mode
        else:
            raise KeyError, 'Wrong key!!!'
        #print request.session.get(request.session.session_key)[123]
    except KeyError, ke:
        #print str(ke)
        mesg = '''\
%s
The trace file was not found -- please run the simulation again.
If the problem still persists, report us back along with this ID:
%s
        ''' % (str(ke), request.session.session_key,)

        error = {'error' : mesg}
        return HttpResponse(json.dumps(error))
    
    except Exception, ex:
        #print str(ex)
        return HttpResponse(ex)

    
    return HttpResponse('Trace file format currently being used: ' + sim_mode)

def general_stats(request):
    #print 'General stats'
    try:
        d = request.session.get(request.session.session_key)
        if d is None:
            raise Exception, INVALID_SESSION_MSG
        if NS_TRACEFILE_KEY in d:
            #print 'Trace file key found'

            if NS_TRACEFILE_MODE in d:
                #print 'Trace file format found (', d[NS_TRACEFILE_MODE], ')'
                # Create a TraceAnalyzer object
                ta = TraceAnalyzer(d[NS_TRACEFILE_KEY], d[NS_TRACEFILE_MODE])
                return HttpResponse(ta.get_statistics())
            else:
                raise KeyError, 'Trace file mode not set!'
        else:
            raise KeyError, 'Wrong key!!!'
        
    except KeyError, ke:
        #print str(ke)
        mesg = str(ke)
        error = {'error' : mesg}
        return HttpResponse(json.dumps(error))
    except Exception, ex:
        #print str(ex)
        return HttpResponse(ex)
     
   
def avg_thruput(request, node_id):
    #print 'Avg thruput'
    try:
        d = request.session.get(request.session.session_key)
        #print d
        if d is None:
            raise Exception, INVALID_SESSION_MSG
        if NS_TRACEFILE_KEY in d:
            #print 'Trace file key found'
            if NS_TRACEFILE_MODE in d:
                #print 'Trace file format found (', d[NS_TRACEFILE_MODE], ')'
                # Create a TraceAnalyzer object
                ta = TraceAnalyzer(d[NS_TRACEFILE_KEY], d[NS_TRACEFILE_MODE])
                return HttpResponse(ta.get_average_throughput_for_node(node_id))
            else:
                raise KeyError, 'Trace file mode not set!'
        else:
            #print 'Trace file key NOT found'
            raise KeyError, 'Wrong key!!!'        
    except KeyError, ke:
        #print str(ke)
        mesg = str(ke)
        error = {'error' : mesg}
        return HttpResponse(json.dumps(error))
    except Exception, ex:
        #print str(ex)
        return HttpResponse(ex)
    

def bytes_received(request, node_id):
    #print 'Bytes received'
    try:
        d = request.session.get(request.session.session_key)
        if d is None:
            raise Exception, INVALID_SESSION_MSG
        if NS_TRACEFILE_KEY in d:
            #print 'Trace file key found'
            if NS_TRACEFILE_MODE in d:
                #print 'Trace file format found (', d[NS_TRACEFILE_MODE], ')'
                # Create a TraceAnalyzer object
                ta = TraceAnalyzer(d[NS_TRACEFILE_KEY], d[NS_TRACEFILE_MODE])
                bytes_rcvd = ta.get_cumulative_bytes_received_for_node(node_id)
                label = 'Bytes received by %s' % node_id
                bytes_rcvd = {
                    'data': bytes_rcvd,
                    'label': label,
                }
                #print bytes_rcvd
                return HttpResponse(json.dumps(bytes_rcvd))
            else:
                raise KeyError, 'Trace file mode not set!'
        else:
            raise KeyError, 'Wrong key!!!'
    except KeyError, ke:
        #print str(ke)
        mesg = str(ke)
        error = {'error' : mesg}
        return HttpResponse(json.dumps(error))
    except Exception, ex:
        #print str(ex)
        return HttpResponse(ex)


def bytes_received_at_levels(request, node_id, levels):
    #print 'Bytes received at levels', levels
    try:
        d = request.session.get(request.session.session_key)
        if d is None:
            raise Exception, INVALID_SESSION_MSG
        if NS_TRACEFILE_KEY in d:
            #print 'Trace file key found'
            if NS_TRACEFILE_MODE in d:

                if levels == 'X':
                    layers = []
                else:
                    layers = levels.split('|')
                    #print 'web_views::', layers
                    layers = [ l.strip() for l in layers if l.strip() != '' ]
                    #print 'web_views::', layers

                # Create a TraceAnalyzer object
                ta = TraceAnalyzer(d[NS_TRACEFILE_KEY], d[NS_TRACEFILE_MODE])
                #print 'web_views:: levels:', levels, ' layers:', layers
                bytes_rcvd = ta.get_cumulative_bytes_received_for_node_at_layers(node_id, layers)
                label = 'Bytes received by %s at %s' % (node_id, levels.replace('|', ',').strip(),)
                bytes_rcvd = {
                    'data': bytes_rcvd,
                    'label': label,
                }
                #print bytes_rcvd
                return HttpResponse(json.dumps(bytes_rcvd))
            else:
                raise KeyError, 'Trace file mode not set!'
        else:
            raise KeyError, 'Wrong key!!!'
    except KeyError, ke:
        #print str(ke)
        mesg = str(ke)
        error = {'error' : mesg}
        return HttpResponse(json.dumps(error))
    except Exception, ex:
        #print str(ex)
        return HttpResponse(ex)


def end2end_delay(request, src_node, dst_node, scale=1):
    #print 'End to end delay'
#    delay = {
#        "label": "Europe (EU27)",
#        "data": [[2751, 0.64323183299999442], [2752, 0.77328405100000452], [2753, 0.78112405099999904], [2756, 0.73195271800000228], [2758, 0.68737403099999739], [2760, 0.67107651999999973], [2762, 0.65437516600000123], [2764, 0.62022398899999587], [2767, 0.58451547900000378], [2769, 0.56797896799999847], [2770, 0.57230247800000456], [2771, 0.58077250000000191], [2776, 0.68640556199999736], [2780, 0.6554085409999999], [2783, 0.65006705200000425], [2784, 0.63822056200000077], [2785, 0.60308569700000447], [2786, 0.65765420800000385], [2791, 0.59578952000000385], [2792, 0.65951869699999577], [2793, 0.66743869700000147], [2794, 0.69967487399999584], [2800, 0.6219700099999983], [2802, 0.60359465599999851], [2803, 0.66222383299999876], [2805, 0.61904514500000118], [2806, 0.61695947900000192], [2807, 0.57244994799999915], [2808, 0.59252294799999561], [2809, 0.57800428099999834], [2810, 0.55562426000000187], [2811, 0.58011094799999796], [2814, 0.57446043699999905], [2816, 0.57275308300000205], [2819, 0.52376957300000271], [2822, 0.45798972900000479], [2823, 0.46584972899999855], [2824, 0.46578972900000082], [2827, 0.42074055199999805], [2831, 0.36246255199999666], [2832, 0.43826590599999804], [2833, 0.44204192599999459], [2838, 0.38499808299999927], [2843, 0.30917106200000433], [2844, 0.31889739500000047], [2845, 0.31894821800000273], [2846, 0.38929559400000358], [2855, 0.26618823999999819], [2856, 0.31073841599999952], [2857, 0.30847274999999996], [2859, 0.3051892599999988], [2865, 0.31848763499999677], [2866, 0.3715149889999978], [2867, 0.37945498899999563], [2868, 0.38502447799999828], [2869, 0.38836914500000574], [2870, 0.49115469699999892], [2873, 0.44023734299999973], [2874, 0.45255034299999863], [2878, 0.41741532200000364], [2879, 0.42772098900000088], [2880, 0.42538547899999912], [2881, 0.43753949999999975], [2882, 0.48628298900000289], [2884, 0.44948496800000015], [2885, 0.50890332299999841], [2886, 0.54331600900000154], [2891, 0.44808361399999797], [2892, 0.44376143700000625], [2893, 0.44165577000000411], [2894, 0.52527194799999677], [2898, 0.53071361399999972], [2899, 0.50365243699999951], [2900, 0.51165243700000218], [2904, 0.51968161399999957], [2906, 0.51317110400000132], [2907, 0.52539494700000233], [2908, 0.60957581200000277], [2911, 0.60755016600000289], [2913, 0.58520881200000474], [2914, 0.58552981200000431], [2919, 0.5446958120000005], [2920, 0.55510383300000399], [2921, 0.56302383199999895], [2922, 0.56557883199999992], [2924, 0.5835675000000009], [2925, 0.60109983200000272], [2926, 0.59083249900000112], [2930, 0.54500765600000278], [2933, 0.5306696560000006], [2935, 0.5818320099999994], [2936, 0.57998634300000163], [2937, 0.56317083300000093], [2938, 0.63530885299999795], [2940, 0.58451967599999932], [2941, 0.55981298900000098], [2942, 0.58432949899999898], [2950, 0.57540083299999623], [2951, 0.57564083300000135], [2952, 0.57536967700000474], [2954, 0.55075552000000272], [2957, 0.62794505099999753], [2958, 0.63356320700000168], [2959, 0.64559722799999975], [2962, 0.62345354099999639], [2963, 0.57257518699999821], [2964, 0.57018951999999956], [2968, 0.54802918699999736], [2969, 0.57073585299999507], [2970, 0.59422669700000341], [2975, 0.60293105200000241], [2976, 0.61321738500000578], [2977, 0.57881418600000245], [2978, 0.68305087399999564], [2979, 0.67310354100000325], [2983, 0.62869403100000198], [2985, 0.58755185400000443], [2986, 0.59747852099999932], [2987, 0.60979220800000178], [2988, 0.60585636399999743], [2991, 0.59547400900000014], [2996, 0.58566667600000244], [2998, 0.5648574989999986], [2999, 0.66385269700000293], [3002, 0.62117234400000143], [3003, 0.60889934300000448], [3004, 0.59006798899999779], [3005, 0.58568581199999414], [3006, 0.60218432199999938], [3010, 0.6041506769999998], [3011, 0.72581320800000526], [3012, 0.72603387499999883], [3015, 0.70532956200000285], [3017, 0.72566438500000174], [3021, 0.67232051999999953], [3022, 0.68242618700000435], [3023, 0.70711052000000052], [3026, 0.63174449899999985], [3027, 0.69744601000000017], [3028, 0.70962985399999923], [3031, 0.73607101000000341], [3037, 0.62897183300000137], [3038, 0.68874952000000178], [3040, 0.6721946970000019], [3041, 0.73114254099999698], [3043, 0.68840183300000035], [3044, 0.64404149899999652], [3045, 0.6792446769999998], [3046, 0.71322820800000386], [3048, 0.7025910309999972], [3050, 0.6702811870000005]]
#    }
#    print json.dumps(delay)
#    return HttpResponse(json.dumps(delay))

    try:
        d = request.session.get(request.session.session_key)
        if d is None:
            raise Exception, INVALID_SESSION_MSG
        if NS_TRACEFILE_KEY in d:
            #print 'Trace file key found'
            if NS_TRACEFILE_MODE in d:
                #print 'Trace file format found (', d[NS_TRACEFILE_MODE], ')'
                # Create a TraceAnalyzer object
                ta = TraceAnalyzer(d[NS_TRACEFILE_KEY], d[NS_TRACEFILE_MODE])
                delay = ta.get_end2end_delay(src_node, dst_node)
                scale = float(scale)
                #print delay[:20]
                delay = [ (seq, scale * e2ed) for (seq, e2ed) in delay ]
                # (Rev #28: #2)
                delay_updt = [ ]
                for (seq, e2ed) in delay:
                    if e2ed < 0:
                        delay_updt.append( (seq, -0.05) )
                    else:
                        delay_updt.append( (seq, e2ed) )
                #print delay_updt[:20]
                # Prepare output data as JSON
                label = 'End to end delay for %s-%s' % (src_node, dst_node,)
                delay = {
                    'label':    label,
                    'data':     delay_updt,
                }
                #print json.dumps(delay)
                return HttpResponse(json.dumps(delay))
            else:
                raise KeyError, 'Trace file mode not set!'
        else:
            raise KeyError, 'Wrong key!!!'
    except KeyError, ke:
        #print str(ke)
        mesg = str(ke)
        error = {'error' : mesg}
        return HttpResponse(json.dumps(error))
    except Exception, ex:
        #print str(ex)
        return HttpResponse(ex)
    

def pkt_retransmits(request, src_node, dst_node):
    #print 'Pkt retransmits'
    try:
        d = request.session.get(request.session.session_key)
        if d is None:            
            raise Exception, INVALID_SESSION_MSG
        if NS_TRACEFILE_KEY in d:
            #print 'Trace file key found'
            if NS_TRACEFILE_MODE in d:
                #print 'Trace file format found (', d[NS_TRACEFILE_MODE], ')'
                # Create a TraceAnalyzer object
                ta = TraceAnalyzer(d[NS_TRACEFILE_KEY], d[NS_TRACEFILE_MODE])
                retransmits = ta.get_packet_retransmissions(src_node, dst_node)
                label = 'Packet retransmission count between %s-%s' % (src_node, dst_node,)
                retransmits = {
                    'data': retransmits,
                    'label': label,
                }
                #print retransmits
                return HttpResponse(json.dumps(retransmits))
            else:
                raise KeyError, 'Trace file mode not set!'
        else:
            raise KeyError, 'Wrong key!!!'
    except KeyError, ke:
        #print str(ke)
        mesg = str(ke)
        error = {'error' : mesg}
        return HttpResponse(json.dumps(error))
    except Exception, ex:
        #print str(ex)
        return HttpResponse(ex)


def clear_session(request):
    #print 'Current session:', request.session.get(request.session.session_key)
    request.session[request.session.session_key] = None
    #print 'Cleared session:', request.session.get(request.session.session_key)
    return HttpResponse('Session cleared! Run the simulation again.')


# (Rev #28 : #3)
def hop_count_pkt_seq_num(request, src_node, src_port, dst_node, dst_port):
    #print 'hop count vs pkt seq #'
    try:
        d = request.session.get(request.session.session_key)
        if d is None:            
            raise Exception, INVALID_SESSION_MSG
        if NS_TRACEFILE_KEY in d:
            #print 'Trace file key found'
            if NS_TRACEFILE_MODE in d:
                #print 'Trace file format found (', d[NS_TRACEFILE_MODE], ')'
                # Create a TraceAnalyzer object
                ta = TraceAnalyzer(d[NS_TRACEFILE_KEY], d[NS_TRACEFILE_MODE])
                count = ta.get_hop_count_pkt_seq_num(int(src_node), int(src_port), int(dst_node), int(dst_port))
                #print 'Count', count[:20]
                label = 'Hop count between %s:%s - %s:%s' % (src_node, src_port, dst_node, dst_port,)
                count = {
                    'data': count,
                    'label': label,
                }                
                #print json.dumps(count)
                return HttpResponse(json.dumps(count))
            else:
                raise KeyError, 'Trace file mode not set!'
        else:
            raise KeyError, 'Wrong key!!!'
    except KeyError, ke:
        #print str(ke)
        mesg = str(ke)
        error = {'error' : mesg}
        return HttpResponse(json.dumps(error))
    except Exception, ex:
        #print str(ex)
        return HttpResponse(ex)
