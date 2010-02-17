from datetime import datetime
import time, os
import json

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.utils.datastructures import MultiValueDictKeyError
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext

from orders.models import BaseOrder, WorkingOrder

from models import DesignPackage
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

    context = {}
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
        
    context['order'] = order
    context['form'] = form

    context.update(extra_context)
                        
    return render_to_response(template, context, context_instance=RequestContext(request))


def update_package(request, packageid, template='packages/update_package.html', extra_context={}):
    
    context = {}
    
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
            
    context['package'] = package
    context['order'] = package.order    
    context['form'] = form

    context.update(extra_context)
                        
    return render_to_response(template, context, context_instance=RequestContext(request))

def list_package_files(request, packageid):
    def gen_file_info(file, name=None):
        path, url, name = file.file.name, file.url, name or os.path.basename(file)
        mt = os.stat(path).st_mtime
        fmt = time.strftime("%M/%d/%Y %I:%M:%S %p",time.localtime(mt))
        return {'name': name,'url': url, 'mod_time': mt, 'formatted_time': fmt }
    
    package = get_object_or_404(DesignPackage, id=packageid)
    package_obj = { 'kit':      gen_file_info(package.kitfile, "2020.kit"),
                    'quote':    package.quotefile 
                                    and gen_file_info(package.quotefile.file, "price_list.pdf") 
                                    or  {},
                    'files':    [ gen_file_info(file.design_file) for file in package.presentation_files.all() ] 
                }
    return HttpResponse(json.dumps(package_obj), content_type='application/json')        

def upload_package_files(request, package_id, file_type='presentation'):
    print "uploading %s" % request        
    if request.method == 'POST': 
        print 'Uploading package_id=%s' % package_id
        print request.POST
    return HttpResponse("1", status=200)

def delete_file(request, packageid):
    raise NotImplemented()