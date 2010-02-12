from datetime import datetime

from django.http import HttpRequest, HttpResponse
from forms import NewPackageForm, PackageFilesForm
from models import WorkingOrder
from design_pack import DesignPackage

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
    
@render_to('packages/update_package.html')
def create_package(request, orderid=None, package_id=None, extra_context={}):
    if not package_id:
        package = DesignPackage.objects.create()
    pkgdataform = NewPackageForm(orderid=orderid)
    stdfilesform = PackageFilesForm()
    
    user = { 'order': None, 'package': None, 'attachments': None }    
    context = { 'packageform': pkgdataform, 'filesform': stdfilesform, 'user': user, 'package': { 'id': 1, 'attachments': [] }  }
        
    return context

def upload_files(request, package_id, file_type='presentation'):
    print "uploading %s" % request        
    if request.method == 'POST': 
        print 'Uploading package_id=%s' % package_id
    return HttpResponse("1", status=200)