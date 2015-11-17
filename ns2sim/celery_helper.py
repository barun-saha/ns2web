author__= "barun"
date__  = "$3 Sep, 2011 11:38:54 PM$"

from django.http import HttpResponse, HttpResponseRedirect
from ns2web.ns2sim import tasks
import celery
import json

# Submit a task and return it's UUID
def celery_submit(request, x, y):
    result = tasks.celery_add.delay(x, y)    
    #print 'Task #:', result.task_id        
    return HttpResponse('Job # %s posted' % (result.task_id,) )    



# Return current state of a task
def task_state(request, uuid):
    output = { 'state': celery.result.AsyncResult(uuid).state }
    return HttpResponse( json.dumps(output) )

def is_task_done(request, uuid):
    return HttpResponse( {'done': celery.result.AsyncResult(uuid).ready() } )

# Return result of the task if done
# Otherwise a message is sent back
def task_result(request, uuid):    
    if celery.result.AsyncResult(uuid).ready():
        output = celery.result.AsyncResult(uuid).get()
        # Store the physical path of the trace file in seesion
        # and remove it from output
        if 'trace_file_name' in output:
            request.session[request.session.session_key] = {'trace_file_name' : output['trace_file_name']}
            #print 'Session:', request.session
            output.pop('trace_file_name')
        #print 'Output:', json.dumps(output)
    else:
        output = {'mesg': 'Still working ...'}        
        
    return HttpResponse( json.dumps(output) )