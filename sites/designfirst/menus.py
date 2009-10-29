from menu import menus
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

menus['dealer'] = lambda: (
    (_('Dashboard'), reverse('dealer-dashboard')),
    (_('New order'), reverse('new_order')),
    (_('Purchase Designs'), reverse('select_products')),
    (_('Profile'), reverse('dealer-complete-profile')),
    # (_('Account'), reverse('')),
    # (_('With submenu'), (
    #     (_('Dashboard'), reverse('dealer-dashboard')),
    #     (_('New order'), reverse('new_order')),
    #     (_('Purchase Designs'), reverse('select_products')),
    #     ))
)


menus['admin'] = lambda: (
    (_('Dashboard'), reverse('dealer-dashboard')),
    (_('Process Registration'), reverse('registration_unauthorized')),
    # Process Fax
    # Customer Info
    # Profile
)
