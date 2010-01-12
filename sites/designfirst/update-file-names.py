import os
import re

from django.conf import settings

from orders.models import Attachment


pat = re.compile('[^\b\w\.]')

for item in Attachment.objects.all():
    path, name = os.path.split(item.file.name)
    safename = pat.sub('_', name)
    if name == safename:
        print 'INFO: skipping %s' % name
        continue
    oldpath = os.path.join(settings.APP_FILES_ROOT, path, name)
    if not os.path.isfile(oldpath):
        print 'ERROR: Attachment %d - File %s doesnt exist.' % (item.id, oldpath)
        continue
    newpath = os.path.join(settings.APP_FILES_ROOT, path, safename)
    while os.path.exists(newpath):
        safename = '_' + safename
        newpath = os.path.join(settings.APP_FILES_ROOT, path, safename)
    print 'moving %s --> \n\t%s' % (oldpath, newpath)
    os.rename(oldpath, newpath)
    itemid = item.id
    item.file.name = os.path.join(path, os.path.basename(newpath))
    item.save()
    check = Attachment.objects.get(pk=itemid)
    f = check.file.open()
