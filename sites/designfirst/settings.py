# Django settings for designfirst project.
import os, sys

THIS_DIR = os.path.abspath(os.path.dirname(__file__))

#Realtive path helper
def rel(*x):
    return os.path.abspath(os.path.join(THIS_DIR, *x))

sys.path.insert(0, rel('..', '..', 'lib'))      #Adding lib to system path

DEBUG = True
DEBUGTOOL = False
LOCAL = True
TEMPLATE_DEBUG = DEBUG
INTERNAL_IPS = ('127.0.0.1',)
SECURE = False

APP_FILES_ROOT = rel('..','..','var','designfirst','files')
APP_FILES_URL = '/files'

##
## PRODUCTION EMAIL SETUP
##
ADMINS = (
    ('Design Service USA Support', 'support@designserviceusa.com'),
    ('Bill Jones', 'bill@averline.com'),
)

MANAGERS = (
    ('Bill Jones', 'bill@designserviceusa.com'),
    ('Barry Tarzy', 'barry@designserviceusa.com'),
    ('Chris Ingram', 'chris@designserviceusa.com'),
    ('Jim Tarzy', 'jim@designserviceusa.com'),
    ('Jeff Stone', 'jeff@designserviceusa.com'),
    ('Design Service USA Support', 'support@designserviceusa.com'),
)

SUPPORT_EMAIL='support@designserviceusa.com'
NOREPLY_EMAIL='no-reply@designserviceusa.com'
DEFAULT_FROM_EMAIL='site-managers@www.designserviceusa.com'
SERVER_EMAIL='site-admin@www.designserviceusa.com'
EMAIL_SUBJECT_PREFIX='[DSUSA]: '

EMAIL_HOST='m0.designserviceusa.com'

##
## PRODUCTION DATABASE SETUP
##
DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = rel('designfirst.db')             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1
USE_I18N = True
MEDIA_ROOT = rel('..', '..', 'static')

MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'd#e-f*3^321$mm_lk0%*t*k!&bo*up*)($g!cv9=7n@1ko!0p7'



# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

# default :
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    # "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
)


TEMPLATE_DIRS = (
    rel('templates'),
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'customer.auth.DealerBackend',
)

ROOT_URLCONF = 'designfirst.urls'
AUTH_PROFILE_MODULE = "customer.UserProfile"
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'paypal.standard.ipn',
    'paypal.standard', 
    'paypal.pro', 
    'ajax_forms',
    'menu',
    'registration',
    'south',
    'notification',
    'designfirst.customer',
    'designfirst.product',
    'designfirst.orders',
    'designfirst.accounting',
    'designfirst.catalog',
    'designfirst.barcode',
    'test',
)

if DEBUGTOOL:
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ) 
    INSTALLED_APPS += ( 
        'debug_toolbar',
    )
    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.version.VersionDebugPanel',
        'debug_toolbar.panels.timer.TimerDebugPanel',
        'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
        'debug_toolbar.panels.headers.HeaderDebugPanel',
        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        'debug_toolbar.panels.template.TemplateDebugPanel',
        'debug_toolbar.panels.sql.SQLDebugPanel',
        'debug_toolbar.panels.signals.SignalDebugPanel',
        'debug_toolbar.panels.logger.LoggingPanel',
    )
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }


APPLICATION_FILES_ROOT = rel('..','..','var','application-data')
APPLICATION_FILES_URL  = rel('..','..','var','application-data')

##
PAYPAL_TEST                 = True      # Testing mode on
if PAYPAL_TEST:
    PAYPAL_WPP_USER         = "cosell_1252871123_biz_api1.averline.com"     # Get from PayPal
    PAYPAL_WPP_PASSWORD     = "1252871133"
    PAYPAL_WPP_SIGNATURE    = "AK62IJSoShoKOn0SppTVKGQxFbWQA6zEuyvKae7yXFouidPif83wSYxC"
    PAYPAL_RECEIVER_EMAIL   = "cosell_1252871123_biz@averline.com"
else:
    PAYPAL_WPP_USER         = ""     # Get from PayPal
    PAYPAL_WPP_PASSWORD     = ""
    PAYPAL_WPP_SIGNATURE    = ""
    PAYPAL_RECEIVER_EMAIL   = ""

# system mail parameters
MAIL_SYSTEM_REPLYTO_ADDRESS = 'system@designserviceusa.com'
MAIL_SYSTEM_NOTIFY_ADDRESS = 'system@designserviceusa.com'

# demo settings (stuff to replace with real code later..)
DEMO_MAIL_DESIGNER_ADDRESS = 'designer-notify@designserviceusa.com'
#DEMO_MAIL_DEALER_ADDRESS = 'dealer-notify@designserviceusa.com'

ACCOUNT_ACTIVATION_DAYS=2
REGISTRATION_AUTHORIZATION = True
SESSION_EXPIRE_AT_BROWSER_CLOSE=True

##
## Settings to control image processing module
##

#PPM_TMP_ROOT = os.path.join(APP_FILES_ROOT, 'tmp')
import tempfile
PPM_TMP_ROOT = tempfile.mkdtemp(suffix='-imgtmp')

try:
    from settings_local import *
except ImportError:
    pass

