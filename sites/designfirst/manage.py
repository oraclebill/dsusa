#!/usr/bin/env python 
import sys; 
import os.path;

_project=os.path.dirname(os.path.abspath(__file__))
_root=os.path.join(_project, '..', '..')

local_path=[ os.path.join(_root,'lib'),  ]

sys.path = local_path + sys.path

from django.core.management import execute_manager

try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)
    
# Make pydev debugger works for auto reload.
try:
    import pydevd
    
    from django.utils import autoreload
    m = autoreload.main
    def main(main_func, args=None, kwargs=None):
        import os
        if os.environ.get("RUN_MAIN") == "true":
            def pydevdDecorator(func):
                def wrap(*args, **kws):
                    pydevd.settrace(suspend=False, port=5678)
                    return func(*args, **kws)
                return wrap
            main_func = pydevdDecorator(main_func)
    
        return m(main_func, args, kwargs)
    
    autoreload.main = main

except ImportError:
#    sys.stderr.write("Error: " +
#        "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")
#    sys.exit(1)
    pass
       
if __name__ == "__main__":
    execute_manager(settings)
