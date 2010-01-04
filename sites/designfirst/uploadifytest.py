from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

from uploadify.views import upload_recieved

def upload_received_handler(sender, data, folder, **kwargs):
    [ kwargs.pop(k,None) for k in ('signal', 'Upload', 'Filename')]
    print '\n==============> kwargs: %s' % kwargs
    print '------------------------------------------------\n'
    print '==============> Name: %s' % data._name
    print '==============> File: %s' % data.file
    print '==============> Folder: %s' % folder
    print '==============> Size: %d' % data._size
    print ' ------------------------------------------------ '
    print '==============> All: %s' % vars(data)
    
upload_recieved.connect(upload_received_handler, dispatch_uid='designfirst.uploadifytest' ) 

def view1(request):
    return render_to_response('uploadifytest1.html', {'uploadify_script_data': "'test': 'Yea!@'" })

def view2(request):
    context={'uploadId': '/random-string/%s' % request.user,
             'uploadify_script_data': "'test': 'Yea!@'" 
    }
    
    return render_to_response('uploadifytest2.html', context, context_instance=RequestContext(request))

def com_view(request):
    return HttpResponse('<p>Gotcha Bitch!</p>')