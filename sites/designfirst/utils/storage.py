import os.path 
import urlparse

from django.core.files.storage import FileSystemStorage
from django.conf import settings

class AppStorage(FileSystemStorage):
    def __init__(self): 
        super(AppStorage, self).__init__(
            location=getattr(settings, 'APP_FILES_ROOT', settings.MEDIA_ROOT), 
            base_url=getattr(settings, 'APP_FILES_URL', settings.MEDIA_URL)       
        )
        
    def url(self,name):
        if not self.base_url or urlparse.urlparse(self.base_url).scheme:
            return super(AppStorage, self).url(name)
        return os.path.join(self.base_url, name)
        
