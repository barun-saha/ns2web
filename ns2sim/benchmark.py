author__= "barun"
date__  = "$3 Sep, 2011 11:38:54 PM$"

from django.http import HttpResponse, HttpResponseRedirect
from ns2web.ns2sim import tasks
import celery

# Submit a task and return it's UUID
def celery_submit(request, x, y):
    result = tasks.celery_add.delay(x, y)
    #print '<b>%d</b>' % (result.get(),)
    print 'Task #:', result.task_id        
    return HttpResponse('Job # %s posted' % (result.task_id,) )    

# Return current state of a task
def task_state(request, uuid):
    return HttpResponse(celery.result.AsyncResult(uuid).state)

def is_done(request, uuid):
    return HttpResponse(celery.result.AsyncResult(uuid).ready())

# Return result of the task if done
# Otherwise a message is sent back
def get_result(request, uuid):
    if celery.result.AsyncResult(uuid).ready():
        return HttpResponse(celery.result.AsyncResult(uuid).get())
    else:
        return HttpResponse('...')