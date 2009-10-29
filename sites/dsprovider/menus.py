from menu import menus
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

#lambda is needed to prevent running reverse until urlpatterns are loaded
menus['base'] = lambda: (
    (_('Dashboard'), reverse('dashboard')),
    (_('Order log'), reverse('order_log')),
    # (_('With submenu'), (
    #     (_('Dashboard'), reverse('dashboard')),
    #     (_('Order log'), reverse('order_log')),
    # ))
)
