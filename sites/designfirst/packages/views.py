from datetime import datetime
import time, os
import json

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponseServerError, HttpResponseForbidden, Http404, HttpResponseNotAllowed
from django.utils.datastructures import MultiValueDictKeyError
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext

from orders.models import BaseOrder, WorkingOrder

from models import DesignPackage, DesignPackageFile
from forms import NewForm, UpdateForm

from utils.views import render_to


        
#class ViewClass(object):
#    
#    def __init__(self, *args, **kwargs):
#        super(ViewClass, self).__init__()
#        
#    def __call__(self, request, *args, **kwargs):
#        http_method = request.method.lower()
#        method = getattr(self, 'process_%s' % http_method )
#        return method(*args, **kwargs)
#        
#class PackageView(ViewClass):
#    def __init__(self, *args, **kwargs):
#        super(PackageView, self).__init__()
#    
#    def handle_post(self, ):
#        pass
    
    
def create_package(request, orderid=None, template='packages/create_package.html', extra_context={}):

    try:
        if not orderid:
            orderid = int(request.GET['oid'])   
    except (ValueError, MultiValueDictKeyError):
        raise Http404('No order specified')

    order = get_object_or_404(WorkingOrder, id=orderid)
    
    if order.status not in (BaseOrder.Const.ASSIGNED, BaseOrder.Const.COMPLETED):
        return HttpResponseForbidden('Invalid order state (%s).' % order.get_status_display() )
        
    if 'GET' == request.method:
        form = NewForm()
    else:
        form = NewForm(request.POST, request.FILES)
        if form.is_valid():
            package = form.save(commit=False)
            package.order = order
            package.save()            
            return HttpResponseRedirect(reverse('update-package', kwargs={'packageid': package.id}))            
            
    # hack a useful 'product type' display
    if order.color_views:
        order.product_type = 'Presentation Pack'
    else:
        order.product_type = 'Pro Design'
        
        
    context = {'order': order, 'form': form }        
    context.update(extra_context)
                        
    return render_to_response(template, context, context_instance=RequestContext(request))


def update_package(request, packageid, template='packages/update_package.html', extra_context={}):
    
    package = get_object_or_404(DesignPackage, id=packageid)
    order = package.order
    
    if order.status not in (BaseOrder.Const.ASSIGNED, BaseOrder.Const.COMPLETED):
        return HttpResponseForbidden('Invalid order state (%s).' % order.get_status_display() )
        
    if 'GET' == request.method:
        form = UpdateForm(instance=package)
    else:
        form = UpdateForm(request.POST, instance=package)
        if form.is_valid():
            package = form.save()
            return HttpResponseRedirect(reverse('update-package', kwargs={'packageid': package.id}))            
            
            
    context = {'package':   package, 
               'order':     order, 
               'form':      form, 
               'update_url':        reverse( 'update-package', args=[packageid, ] ),  
               'list_files_url':    reverse( 'package-files-list', args=[packageid, ] ),  
               'upload_files_url':  reverse( 'package-files-upload', args=[packageid, ] ),
    }
    context.update(extra_context)
                        
    return render_to_response(template, context, context_instance=RequestContext(request))




def list_package_files(request, packageid):
        
    def gen_file_info(file, name=None, id=None):
        print 'file >> %s' % file
        path, url, name = file.file.name, file.url, name or os.path.basename(file.path)
        mt = os.stat(path).st_mtime
        if datetime.fromtimestamp(mt) == datetime.today():
            fmt = time.strftime("%I:%M %p",time.localtime(mt))
        else:
            fmt = time.strftime("%b %d, %Y",time.localtime(mt))
        return  {'id': id, 'name': name,'url': url, 'mod_time': mt, 'formatted_time': fmt }
    
    package = get_object_or_404(DesignPackage, id=packageid)
    package_obj = { 'kit':      gen_file_info(package.kitfile, "2020.kit"),
                    'quote':    package.quotefile 
                                    and gen_file_info(package.quotefile, "price_list.pdf") 
                                    or  {},
                    'files':    [ gen_file_info(file.design_file, id=file.id) for file in package.presentation_files.all() ] 
                }
    return HttpResponse(json.dumps(package_obj), content_type='application/json')        

    
    
def upload_package_files(request, package_id, file_type='presentation'):
    
    print ' -- > uplaod called with  %s\n%s' % (request.FILES, request.POST)
         
    package = get_object_or_404(DesignPackage, id=package_id)    
    if request.method == 'POST':
        if request.FILES:
            filedata = request.FILES['Filedata']
            filename = request.POST['Filename']
            folder = request.POST['folder']

            print "(%s, %s, %s)" % ( folder, filename, len(filedata))
            # update package for core files
            if folder.endswith('core'):
                print 'CORE'
                if filename.lower().endswith('.kit'): 
                    print 'KIT'
                    package.kitfile = filedata
                else:
                    package.quotefile = filedata 
                package.save()    
            # add new 'designfile' for others                 
            else:
                new_file = DesignPackageFile(
                                design_package = package,
                                design_file = filedata,
                                file_type = DesignPackageFile.Const.PERSPECTIVE
                )
                new_file.save()           
                #new_file.design_file.close()
            return HttpResponse('1')
        else:
            return HttpResponseServerError('missing files')    
    else:
        return HttpResponseNotAllowed(request.method)


def delete_file(request, packageid):
    raise NotImplemented()


def serve_file(request, package_id, file_id):
    package = get_object_or_404(DesignPackage, id=package_id)
    package_file = get_object_or_404(DesignPackageFile, id=file_id)
    
    ## TODO: security
    
    if request.method == 'GET':
        return HttpResponseRedirect(package_file.design_file.url)
    elif request.method == 'POST' or request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass
    
    return HttpResponse 

    
