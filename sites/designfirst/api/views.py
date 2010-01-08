import logging
from xml.etree import ElementTree as etree

from django.http import HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponse

from models import *

logger = logging.getLogger('api.views')

def process_inbound_fax(request):
    logger.debug('process_inbound_fax: processing %s', request)
    if request.method != 'POST':
        return HttpResponseNotAllowed('post only')
    xml = request.POST['xml']
    try:
        fax = _parse_efax_xml(xml)
        fax.save()
        logger.debug('process_inbound_fax: fax %s processed successfully', fax)
    except Exception as ex:        
        return HttpResponseBadRequest(ex)
    
    return HttpResponse('Post Successful')