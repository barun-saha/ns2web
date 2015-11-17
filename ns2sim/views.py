# ns2

from django.http import HttpRequest
from django.core.context_processors import request
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.conf import settings
import os
import re
import json

#from recaptcha.client import captcha
from ns2web.ns2sim import tasks
import celery

import time
import celery_helper
import globals
import glob
import settings

import celery


def index(request):
    '''
    Home page -- display the interface
    '''
    #t = Theory.objects.all()    
    return render_to_response(
        'ns2/ns2_interface.html',
        {},
        context_instance=RequestContext(request)
    )


def batch(request):
    return render_to_response(
        'ns2/ns2_interface_batch.html',
        {},
        context_instance=RequestContext(request)
    )
    

# Submit a Celery task to execute ns2 code    
# Returns UUID of the created task
def ns2run(request):
    output = {}
    if request.method == 'POST':
        #print 'Sumitting task ...'
        code = request.POST.get('ns2code')
        session_key = request.session.session_key
        new_task = tasks.ns2run.delay(code, session_key)
        #print '<b>%d</b>' % (result.get(),)
        #print 'Simulation # :', new_task.task_id 
        output['id'] = new_task.task_id        
    else:
        output['error'] = 'Invalid attempt to access a resource!'        

    return HttpResponse( json.dumps(output) )


# Batch mode simulation
def ns2run_batch(request):
    output = {}
    if request.method == 'POST':
        #print 'Sumitting task ...'
        code = request.POST.get('ns2code')
        metrics = request.POST.get('metrics')
        #print metrics
        if len(metrics) > 0:
            # One or more analysis metric has been specified
            pass
        
        #return HttpResponseRedirect( metrics )
        session_key = request.session.session_key
        timestamp = time.time()
        task_ref = '-'.join( [session_key, str(timestamp), ] )
        
        new_task = tasks.ns2run_batch.delay(code, session_key, timestamp, metrics)
        
        #print '<b>%d</b>' % (result.get(),)
        #print 'Simulation # :', new_task.task_id 
        #output['id'] = task_ref
        #output['id'] = new_task.task_id
        output['id'] = '/'.join( [ session_key, str(timestamp), new_task.task_id, ] )
    else:
        output['error'] = 'Invalid attempt to access a resource!'        

    return HttpResponse( json.dumps(output) )
    


# Batch mode simulation result
def batch_result(request, session_key=None, timestamp=None, task_id=None):
    html_templ = ''
    
    if not session_key or not timestamp or not task_id:
        html_templ = 'An error occured!'
    else:        
        task_status = celery.result.AsyncResult(task_id).state        

        if task_status.upper() == 'SUCCESS':
            metrics_dir_path = '/'.join( [globals.NS2_SCRIPT_STORAGE_PATH, 'batch', session_key, timestamp, 'metrics',] )         
            all_img_files = glob.glob(metrics_dir_path + '/*.png')

            media_path = settings.MEDIA_URL
            media_url = media_path
            if settings.__ENV_PROD__:
                media_url += 'ns2web/batch/'
            else:
                media_url += 'ns2web_demo/batch/'

            media_url += session_key+'/'+timestamp+'/metrics/';
            
            img_templ = '<img src="%s">'
            html_templ = ''
            if len(all_img_files) > 0:
                for an_img in all_img_files:        
                    an_img = an_img[ an_img.rindex('/')+1: ]
                    #print an_img
                    html_templ += img_templ % (media_url + an_img,)
            else:
                html_templ = 'No graph has been generated! Please make sure your simulation script is correct. Also, it is possible that no data for plot could be found for the analysis metrics you have chosen.'
        else:
            html_templ = 'The simulation is still running. Please refresh this page after few moments.'            

    return HttpResponse(html_templ)        

