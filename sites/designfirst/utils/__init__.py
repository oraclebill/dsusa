from django.contrib.sites.models import Site
from django.conf import settings

def make_site_url(path):
    scheme = settings.SECURE and 'https' or 'http'
    domain = Site.objects.get_current().domain.rstrip('/')    
    return '%s://%s/%s' % (scheme, domain, path.lstrip('/'))
    
