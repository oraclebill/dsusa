# Django settings for designfirst project.
import os, sys

THIS_DIR = os.path.abspath(os.path.dirname(__file__))

#Realtive path helper
def rel(*x):
    return os.path.abspath(os.path.join(THIS_DIR, *x))

sys.path.insert(0, rel('..', '..', 'lib'))#Adding lib to system path




DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)
MANAGERS = ADMINS


DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = rel('designfirst.db')             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/NewYork'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1001

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = rel('..', '..', 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
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
    "django.core.context_processors.media"
)


TEMPLATE_DIRS = (
    rel('templates'),
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'designfirst.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'designfirst.home',
    'designfirst.designer',
    'designfirst.product',
    'designfirst.wizard',
    'debug_toolbar',
    'paypal.standard.ipn',
    'paypal.standard', 
    'paypal.pro', 
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

AUTH_PROFILE_MODULE = "home.UserProfile"


# PAYPAL_TEST             = True      # Testing mode on
# PAYPAL_WPP_USER         = "seller_1252615556_biz_api1.averline.com"     # Get from PayPal
# PAYPAL_WPP_PASSWORD     = "1252615561"
# PAYPAL_WPP_SIGNATURE    = "AQU0e5vuZCvSg-XJploSa.sGUDlpAgc.wJ13tW2dLYqGl34E.D940-.6"
# PAYPAL_RECEIVER_EMAIL   = "seller_1252615556_biz@averline.com"

##
PAYPAL_TEST             = True      # Testing mode on
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


try:
    from settings_local import *
except ImportError:
    pass