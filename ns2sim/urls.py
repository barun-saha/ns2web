from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import *
#from ns2web.ns2.models import *
from django.conf import settings

urlpatterns = patterns('ns2web.ns2sim.views',
    url(r'^$',                                 'index',         name='index'),
    url(r'^ns2_submit/$',                  'ns2run',),
    url(r'^batch/$',                  'batch',),
    url(r'^batch/ns2_submit/$',                  'ns2run_batch',),
    url(r'^batch/result/(?P<session_key>[a-zA-Z0-9\.\-\_]+)/(?P<timestamp>[0-9\.]+)/(?P<task_id>[a-zA-Z0-9\-]+)/$',                  'batch_result',),
)

# Celery related
urlpatterns += patterns('ns2web.ns2sim.celery_helper',        
    url(r'^cel/submit/(?P<x>\d+)/(?P<y>\d+)/$',                  'celery_submit',),
    url(r'^cel/state/(?P<uuid>[a-z0-9\-]+)/$',                  'task_state',),
    url(r'^cel/result/(?P<uuid>[a-z0-9\-]+)/$',                  'task_result',),
)
urlpatterns += patterns('',
    url('^cel/tasks/', include('djcelery.urls')),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^xmedia/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
