from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

import designfirst.menus
from django.views.generic.list_detail import object_detail
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import views as auth_views
from registration import views
from registration import models as reg_models
import forms

from django.contrib import admin
admin.autodiscover()

# import customer.forms

urlpatterns = patterns('',
    # Example:
    # (r'^designfirst/', include('designfirst.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'', include("customer.urls")),    
    (r'^products/', include("product.urls")),    
    (r'^orders/',   include("orders.urls")),
    (r'^accounts/', include('registration.urls')),
    (r'^barcode/',  include("barcode.urls")),        
    (r'^admin/',    include(admin.site.urls)),
    # (r'^60b9f188a8a27ce69fcba9ee63b74b4e2fad2b3d/', include('paypal.standard.ipn.urls')),
)

urlpatterns += patterns('',
    url(r'^accounts/profile/(?P<object_id>\d+)/',
        permission_required('can_authorize')(object_detail), {
            'queryset': reg_models.RegistrationProfile.objects.all(),
            'template_object_name': 'profile',
        }, name='registration_profile'),
   url(r'^activate/register/(?P<activation_key>\w+)/$',
        views.activate_and_register,
        name='registration_activate_and_register'),
    url(r'^accounts/authorized/$',
        views.authorized_profiles_list,
        name='registration_authorized'),
    url(r'^accounts/unauthorized/$',
        views.unauthorized_profiles_list,
        name='registration_unauthorized'),
    url(r'^accounts/authorize/(?P<profile_id>\d+)/$',
        views.authorize,
        name='registration_authorize'),
    url(r'^accounts/login/$',
        auth_views.login,
        {'template_name': 'registration/login.html'},
        name='auth_login'),
    url(r'^accounts/logout/$',
        auth_views.logout,
        {'template_name': 'registration/logout.html'},
        name='auth_logout'),
    url(r'^accounts/password/change/$',
        auth_views.password_change,
        name='auth_password_change'),
    url(r'^accounts/password/change/done/$',
        auth_views.password_change_done,
        name='auth_password_change_done'),
    url(r'^accounts/password/reset/$',
        auth_views.password_reset,
        name='auth_password_reset'),
    url(r'^accounts/password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        name='auth_password_reset_confirm'),
    url(r'^accounts/password/reset/complete/$',
        auth_views.password_reset_complete,
        name='auth_password_reset_complete'),
    url(r'^accounts/password/reset/done/$',
        auth_views.password_reset_done,
        name='auth_password_reset_done'),
    url(r'^accounts/register/$',
        views.register,
        {'form_class': forms.RegistrationForm},
        name='registration_register'),
    url(r'^accounts/register/complete/$',
        direct_to_template,
        {'template': 'registration/registration_complete.html'},
        name='registration_complete'),
)


from django.conf import settings
if settings.DEBUG and settings.LOCAL:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
