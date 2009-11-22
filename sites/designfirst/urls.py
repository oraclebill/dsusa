from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import permission_required
from django.views.generic.list_detail import object_detail
from django.views.generic.simple import direct_to_template

#from registration import views as registration
#from registration import models as reg_models
#import forms

import menus  # remove this import and any page with a {% menu ... %} tag fails.. pretty damn random.. 

from django.contrib import admin
admin.autodiscover()

# import customer.forms

urlpatterns = patterns('',
    (r'', include("customer.urls")),    
    (r'^accounts/', include("customer.registration.urls")),    
    url(r'^profile/$',
        'designfirst.views.profile_edit',
        name='profile_edit'),
    (r'^products/', include("product.urls")),    
    (r'^orders/',   include("orders.urls")),
    (r'^barcode/',  include("barcode.urls")),        
    (r'^notification/',  include("notification.urls")),        
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/',    include(admin.site.urls)),
)
    
#urlpatterns += patterns('',
#    url(r'^accounts/profile/(?P<object_id>\d+)/',
#        permission_required('can_authorize')(object_detail), {
#            'queryset': reg_models.RegistrationProfile.objects.all(),
#            'template_object_name': 'profile',
#        }, name='registration_profile'),
#   url(r'^activate/register/(?P<activation_key>\w+)/$',
#        registration.activate_and_register,
#       {'success_url': 'profile_edit'},
#        name='registration_activate_and_register'),
#    url(r'^accounts/authorized/$',
#        registration.authorized_profiles_list,
#        name='registration_authorized'),
#    url(r'^accounts/unauthorized/$',
#        registration.unauthorized_profiles_list,
#        name='registration_unauthorized'),
#    url(r'^accounts/authorize/(?P<profile_id>\d+)/$',
#        registration.authorize,
#        name='registration_authorize'),
#    url(r'^accounts/login/$',
#        auth_views.login,
#        {'template_name': 'registration/login.html'},
#        name='auth_login'),
#    url(r'^accounts/logout/$',
#        auth_views.logout,
#        {'template_name': 'registration/logout.html'},
#        name='auth_logout'),
#    url(r'^accounts/password/change/$',
#        auth_views.password_change,
#        name='auth_password_change'),
#    url(r'^accounts/password/change/done/$',
#        auth_views.password_change_done,
#        name='auth_password_change_done'),
#    url(r'^accounts/password/reset/$',
#        auth_views.password_reset,
#        name='auth_password_reset'),
#    url(r'^accounts/password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
#        auth_views.password_reset_confirm,
#        name='auth_password_reset_confirm'),
#    url(r'^accounts/password/reset/complete/$',
#        auth_views.password_reset_complete,
#        name='auth_password_reset_complete'),
#    url(r'^accounts/password/reset/done/$',
#        auth_views.password_reset_done,
#        name='auth_password_reset_done'),
#    url(r'^accounts/register/$',
#        registration.register,
#        {'form_class': forms.RegistrationForm, 'template_name': 'registration/registration_form.html'},
#        name='registration_register'),
#    url(r'^accounts/register/complete/$',
#        direct_to_template,
#        {'template': 'registration/registration_complete.html'},
#        name='registration_complete'),
#)


from django.conf import settings
if settings.DEBUG and settings.LOCAL:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.APP_FILES_ROOT}),
    )
