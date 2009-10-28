from menu import menus
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

menus['base'] = lambda: (
    (_('Dashboard'), reverse('dashboard')),
    (_('Order log'), reverse('order_log')),
    (_('With submenu'), (
        (_('Dashboard'), reverse('dashboard')),
        (_('Order log'), reverse('order_log')),
    ))
)
