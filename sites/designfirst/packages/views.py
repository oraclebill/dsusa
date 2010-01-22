from datetime import datetime

from django.http import HttpRequest
from forms import NewPackageForm
from models import WorkingOrder
from design_pack import DesignPackage

from utils.views import render_to

def _create_package(related_order, related_package, created_by, created_on, notes, version):
    pass
    

@render_to('packages/new_package.html')
def create_package(request, orderid=None, extra_context={}):
#    user = request.user
#    if orderid:
#        order = WorkingOrder.objects.get(pk=orderid)
#        orderpackages = DesignPackage.get_packages_for_order(orderid)
#    else:
#        order = None 
#        
#    context = {'orderid': orderid, 'created_by': user.id, 'created_on': datetime.now(), 'orderpackages': orderpackages }
#    if 'GET' == request.method: 
#        form = NewPackageForm()
#    if 'POST' == request.method:
#        form = NewPackageForm(request.POST)
#        if form.is_valid():
#            related_order   = form['orderid']
#            related_package = form['related_packageid']
#            created_by      = form['created_by']
#            created_on      = form['created_on']
#            notes           = form['notes']
#            version         = form['version']
#            
#            package = _create_package(related_order, related_package, created_by, created_on, notes, version)
    
    user = { 'order': None, 'package': None, 'attachments': None }
    
    context = { }    
    return context