from celery.decorators import task
from django.conf import settings
from django.http import HttpResponse
import time

import subprocess as sp
import os
import re
import json
import globals

from ns2web.ns2trace.trace_analyzer import TraceAnalyzer
import matplotlib.pyplot as plt


#NS_TRACEFILE_KEY    = 'trace_file_name'    # Key to store trace file name in seesion
#TRACE_ANALYZER_KEY  = 'ta_object'        # Key to store TraceAnalyzer object


#@task(name="ns2sim.tasks.celery_add")
#def celery_add(x, y):
#    time.sleep(15)
#    return int(x) + int(y)


@task(name="ns2sim.tasks.ns2run")
def ns2run(code, session_key):
    #code = request.POST.get('ns2code')
    #print 'Session key:', session_key

    script_file_name = 'script_' + session_key
    script_file_path = globals.NS2_SCRIPT_STORAGE_PATH + '/' + session_key + '/' + script_file_name
    user_dir_path = globals.NS2_SCRIPT_STORAGE_PATH + '/' + session_key

    #print script_file_path

    is_error = False
    error_mesg = ''
    script_file = None

    # Store the user program in a temporary file
    try:
        script_file = open(script_file_path, 'w')
        script_file.write(code)
    except IOError, ioe:
        is_error = True
        error_mesg = str(ioe)
        try:
            os.mkdir(user_dir_path)
            script_file = open(script_file_path, 'w')
            script_file.write(code)
            is_error = False
        except OSError, ose:
            is_error = True
            error_mesg = str(ose)
    except Exception, e:
        is_error = True
        error_mesg = str(e)
    finally:
        if script_file:
            script_file.close()
        if is_error:
            return HttpResponse('<p class="error">Error: ' + error_mesg + '</p>')

    is_error = False

    #print 'XXX'
    # Any file set to create within the program will be created at /var/vlabs_demo/ant
    changed_contents = ''
    try:
        script_file = open(script_file_path, 'r')
        changed_contents = re.sub(r'(\[\s*\bopen\s+)\b(.*?)\s+(w\s*\])',
                                r'\1 ' + user_dir_path + r'/\2 \3',
                                script_file.read()
        )
        script_file.close()

        # Disable any exec statement present in the script
        changed_contents = re.sub(r'(\bexec\b)', r'#\1', changed_contents)

        script_file = open(script_file_path, 'w')
        script_file.write(changed_contents)
        script_file.close()
        #print changed_contents
        #return HttpResponse(changed_contents)
    except IOError, ioe:
        is_error = True
        error_mesg = str(ioe)
        return HttpResponse('<p class="error">Error: ' + error_mesg + '</p>')

    # Flags for files
    trace_file_exists = False
    nam_trace_file_exists = False

    # Find the name of the trace file, if any
    trace_file_var = None
    trace_file_name = None
    trace_file_path = None
    mobj = re.search(r'\s*[$]{1}\w+\s+trace-all\s+[$]{1}([\w-]+)', changed_contents)
    if mobj:
        trace_file_var = mobj.group(1)
        declaration_pattern = r'set\s+%s\s+\[\s*open\s+([\w./-]+)\s+w\s*\]' % (trace_file_var,)
        #print declaration_pattern
        mobj = None
        #print changed_contents
        mobj = re.search(declaration_pattern, changed_contents)
        if mobj:
            trace_file_name = mobj.group(1)
            trace_file_exists = True
            #trace_file_path = globals.NS2_SCRIPT_STORAGE_PATH + '/' + session_key + '/' + trace_file_name

    # Generate the argument list
    args = (globals.NS2_PATH, script_file_path,)
    #print args

    # Spawn the sub process
    process = sp.Popen(args, shell=False, stdout=sp.PIPE, stderr=sp.PIPE)
    result, error =  process.communicate()
    #print process.returncode

    if process.returncode != 0:
            mesg = 'An error occured while executing your script!'
            trace_file_exists = False
    else:
            mesg = 'Successful!'

    mesg += '\n' + result
    if error:
        mesg += '\n' + error

    mesg = re.sub(session_key, 'XXX', mesg)     # Hide the session ID
    mesg = re.sub(globals.NS2_SCRIPT_STORAGE_PATH, r'[base]', mesg)         # Hide the server storage path
    #print mesg
    output = {'mesg': mesg,}
    
    #print 'Trace file:', trace_file_name

    if trace_file_exists:
        # *** Store trace file name for the current user session ***
        
        # ??? Trace file name ???
        #request.session[request.session.session_key] = {'trace_file_name' : trace_file_name}
        #
        
        #print request.session.get(request.session.session_key)
        output['trace_file_name'] = trace_file_name

        # Convert physical path of trace file to URL
        output['trace'] = trace_file_name.replace(r'/var/', settings.MEDIA_URL)
        #print trace_file_name
        # Return the contrnts of the trace file
        try:
            tr_file = open(trace_file_name, 'r')
            output['trace'] = tr_file.readlines()
        except IOError, ioe:
            output['error'] = str(ioe)
        finally:
            if tr_file:
                tr_file.close()
    else:
        output['trace'] = ''

    #print 'Output:', output
    return output


@task(name="ns2sim.tasks.ns2run_batch")
def ns2run_batch(code, session_key, timestamp, metrics=[]):
    #code = request.POST.get('ns2code')
    #print 'Session key:', session_key

    timestamp = str(timestamp)

    #script_file_name   = 'script_' + session_key
    script_file_name    = 'script_'
    script_file_path    = globals.NS2_SCRIPT_STORAGE_PATH + '/batch/' + session_key + '/' + timestamp + '/' + script_file_name
    user_dir_path       = globals.NS2_SCRIPT_STORAGE_PATH + '/batch/' + session_key + '/' + timestamp

    #print script_file_path

    is_error = False
    error_mesg = ''
    script_file = None

    # Store the user program in a temporary file
    try:
        #script_file = open(script_file_path, 'w')
        #script_file.write(code)
    #except IOError, ioe:
        #is_error = True
        #error_mesg = str(ioe)
        #try:
        
        os.makedirs(user_dir_path)
        script_file = open(script_file_path, 'w')
        script_file.write(code)
        is_error = False
        
        #except OSError, ose:
            #is_error = True
            #error_mesg = str(ose)
    except Exception, e:
        is_error = True
        error_mesg = str(e)
    finally:
        if script_file:
            script_file.close()
        if is_error:
            return HttpResponse('<p class="error">Error: ' + error_mesg + '</p>')

    is_error = False

    #print 'XXX'
    # Any file set to create within the program will be created at /var/vlabs_demo/ant
    changed_contents = ''
    try:
        script_file = open(script_file_path, 'r')
        changed_contents = re.sub(r'(\[\s*\bopen\s+)\b(.*?)\s+(w\s*\])',
                                r'\1 ' + user_dir_path + r'/\2 \3',
                                script_file.read()
        )
        script_file.close()

        # Disable any exec statement present in the script
        changed_contents = re.sub(r'(\bexec\b)', r'#\1', changed_contents)

        script_file = open(script_file_path, 'w')
        script_file.write(changed_contents)
        script_file.close()
        #print changed_contents
        #return HttpResponse(changed_contents)
    except IOError, ioe:
        #print ioe
        is_error = True
        error_mesg = str(ioe)
        return HttpResponse('<p class="error">Error: ' + error_mesg + '</p>')

    # Flags for files
    trace_file_exists = False
    nam_trace_file_exists = False

    # Find the name of the trace file, if any
    trace_file_var = None
    trace_file_name = None
    trace_file_path = None
    mobj = re.search(r'\s*[$]{1}\w+\s+trace-all\s+[$]{1}([\w-]+)', changed_contents)
    if mobj:
        trace_file_var = mobj.group(1)
        declaration_pattern = r'set\s+%s\s+\[\s*open\s+([\w./-]+)\s+w\s*\]' % (trace_file_var,)
        #print declaration_pattern
        mobj = None
        #print changed_contents
        mobj = re.search(declaration_pattern, changed_contents)
        if mobj:
            trace_file_name = mobj.group(1)
            trace_file_exists = True
            #trace_file_path = globals.NS2_SCRIPT_STORAGE_PATH + '/' + session_key + '/' + trace_file_name

    # Generate the argument list
    args = (globals.NS2_PATH, script_file_path,)
    #print args

    # Spawn the sub process
    process = sp.Popen(args, shell=False, stdout=sp.PIPE, stderr=sp.PIPE)
    result, error =  process.communicate()
    #print process.returncode

    if process.returncode != 0:
        mesg = 'An error occured while executing your script!'
        trace_file_exists = False
    else:
        mesg = 'Successful!'

    mesg += '\n' + result
    if error:
        mesg += '\n' + error

    mesg = re.sub(session_key, 'XXX', mesg)     # Hide the session ID
    mesg = re.sub(globals.NS2_SCRIPT_STORAGE_PATH, r'[base]', mesg)         # Hide the server storage path
    #print mesg
    output = {'mesg': mesg,}
    
    #print 'Trace file:', trace_file_name

    if trace_file_exists:
        # *** Store trace file name for the current user session ***
        
        # ??? Trace file name ???
        #request.session[request.session.session_key] = {'trace_file_name' : trace_file_name}
        #
        
        #print request.session.get(request.session.session_key)
        output['trace_file_name'] = trace_file_name

        # Convert physical path of trace file to URL
        output['trace'] = trace_file_name.replace(r'/var/', settings.MEDIA_URL)
        #print trace_file_name
        
        # Return the contents of the trace file
        #try:
        #    tr_file = open(trace_file_name, 'r')
        #    output['trace'] = tr_file.readlines()
        #except IOError, ioe:
        #    output['error'] = str(ioe)
        #finally:
        #    if tr_file:
        #        tr_file.close()

        if len(metrics) > 0:
            analyze_trace_file(trace_file_name, session_key, timestamp, metrics)
            
    else:
        output['trace'] = ''

    #print 'Output:', output
    #return output



def analyze_trace_file(trace_file_name, session_key, timestamp, metrics):

    metrics_dir_path       = '/'.join( [globals.NS2_SCRIPT_STORAGE_PATH, 'batch', session_key, timestamp, 'metrics',] )
    
    try:
        os.makedirs( metrics_dir_path )
        #print 'Created dir', metrics_dir_path
        
        try:
            tr_file = open(trace_file_name, 'r')
            #print 'Analyzing trace file', trace_file_name

            metrics = json.loads( metrics )
            #print metrics
            for a_metric in metrics:
                a_metric = json.loads( a_metric )
                
                if a_metric['name'] == "bytes-rcvd":

                    # Sample: {"name":"bytes-rcvd","parameters":[66,"MAC|RTR|"],"mode":"Wired"}
                    ta = TraceAnalyzer( trace_file_name, a_metric['mode'] )
                    layers = a_metric['parameters'][1].strip()
                    if len(layers) > 0:
                        layers = [ l.strip() for l in a_metric['parameters'][1].split('|') if l.strip() != '' ]
                    else:
                        layers = None
                    #print layers
                    bytes_rcvd = ta.get_cumulative_bytes_received_for_node_at_layers(a_metric['parameters'][0], layers)
                    #print 'bytes_rcvd', len(bytes_rcvd)
                    xvals = []
                    yvals = []
                    for entry in bytes_rcvd:
                        xvals.append(entry[0])
                        yvals.append(entry[1])

                    image_file_name = '-'.join( [ 'bytes_rcvd', str(a_metric['parameters'][0]), a_metric['parameters'][1].replace('|', '_') ] )
                    image_file_name += '.png'

                    image_title = 'Bytes received by node %d (%s)' % ( a_metric['parameters'][0], a_metric['parameters'][1], )
                                        
                    plot_graph(xvals, yvals, 'Time (in seconds)', 'Kbits received', image_title, metrics_dir_path+'/'+image_file_name)
                    
                elif a_metric['name'] == "e2e-delay":

                    # Sample: {"name":"e2e-delay","parameters":[66,67,1],"mode":"Wired"}
                    ta = TraceAnalyzer( trace_file_name, a_metric['mode'] )
                    delay = ta.get_end2end_delay( a_metric['parameters'][0], a_metric['parameters'][1] )

                    xvals = []
                    yvals = []
                    for entry in delay:
                        xvals.append(entry[0])
                        yvals.append(entry[1])

                    image_file_name = '-'.join( [ 'e2e_delay', str(a_metric['parameters'][0]), str(a_metric['parameters'][1]), str(a_metric['parameters'][2]) ] )
                    image_file_name += '.png'

                    image_title = 'End-to-end delay between nodes %d and %d (scaling = %d)' % (a_metric['parameters'][0], a_metric['parameters'][1], a_metric['parameters'][2])
                                        
                    plot_graph(xvals, yvals, 'Packet sequence #', 'Delay', image_title, metrics_dir_path+'/'+image_file_name)

                elif a_metric['name'] == "pkt-retransmission":

                    # Sample: {"name":"pkt-retransmission","parameters":[66,67],"mode":"Wired"}
                    ta = TraceAnalyzer( trace_file_name, a_metric['mode'] )
                    count = ta.get_packet_retransmissions( a_metric['parameters'][0], a_metric['parameters'][1] )

                    xvals = []
                    yvals = []
                    for entry in count:
                        xvals.append(entry[0])
                        yvals.append(entry[1])

                    image_file_name = '-'.join( [ 'pkt-retransmission', str(a_metric['parameters'][0]), str(a_metric['parameters'][1]), ] )
                    image_file_name += '.png'

                    image_title = 'Packet retransmissions between nodes %d and %d' % ( a_metric['parameters'][0], a_metric['parameters'][1], )

                    plot_graph(xvals, yvals, 'Packet sequence #', 'Retransmission count', image_title, metrics_dir_path+'/'+image_file_name)
                                                            
                elif a_metric['name'] == "hop-count":

                    # Sample: {"name":"hop-count","parameters":[66,0,67,0],"mode":"Wired"}
                    ta = TraceAnalyzer( trace_file_name, a_metric['mode'] )
                    count = ta.get_hop_count_pkt_seq_num( a_metric['parameters'][0], a_metric['parameters'][1], a_metric['parameters'][2], a_metric['parameters'][3] )

                    xvals = []
                    yvals = []
                    for entry in count:
                        xvals.append(entry[0])
                        yvals.append(entry[1])

                    image_file_name = '-'.join( [ 'pkt-retransmission', str(a_metric['parameters'][0]), str(a_metric['parameters'][1]), ] )
                    image_file_name += '.png'

                    image_title = 'Hop count between nodes %d:%d and %d:%d' % ( a_metric['parameters'][0], a_metric['parameters'][1], a_metric['parameters'][2], a_metric['parameters'][2], )
                    
                    plot_graph(xvals, yvals, 'Packet sequence #', 'Hop count', image_title, metrics_dir_path+'/'+image_file_name)
                    
            
        except IOError, ioe:
            output['error'] = str(ioe)
        finally:
            if tr_file:
                tr_file.close()
            
    except OSError, ose:
        pass
        #print 'Failed to create dir ', metrics_dir_path, ose


def plot_graph(xvals, yvals, xlabel, ylabel, title, file_name, transparency = False):
    fig = plt.figure()
    axes = fig.add_subplot(111)

    plt.plot(xvals, yvals)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    axes.set_autoscale_on(True)
    axes.autoscale_view(True, True, True)
    plt.savefig(file_name, transparent = transparency)
