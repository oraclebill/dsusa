from menu import menus
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

#lambda is needed to prevent running reverse until urlpatterns are loaded
menus['dealer'] = lambda: (
    (_('Dashboard'), reverse('dealer-dashboard')),
    (_('New order'), reverse('create-order')),
    (_('Purchase Designs'), reverse('select_products')),
    (_('Profile'), reverse('profile-edit')),
    # (_('Account'), reverse('')),
    # (_('With submenu'), (
    #     (_('Dashboard'), reverse('dealer-dashboard')),
    #     (_('New order'), reverse('create-order')),
    #     (_('Purchase Designs'), reverse('select_products')),
    #     ))
)

menus['limited'] = lambda: (
    (_('Dashboard'), reverse('dealer-dashboard')),
    (_('Profile'), reverse('profile-edit')),
)


menus['admin'] = lambda: (
    (_('Dashboard'), reverse('dealer-dashboard')),
    (_('Process Registration'), reverse('registration_unauthorized')),
    # Process Fax
    # Customer Info
    # Profile
)
