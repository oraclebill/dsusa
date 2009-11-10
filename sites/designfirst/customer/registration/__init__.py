"""
customizations of django-registration for the design service usa dealer site

this backend implements the following workflow -
 1) potential users fill out a comprehensive registration form and submit it for approval as 'registered dealers' 
     a) information from the registration form is used to create a new dealer account in 'pending' status, a primary account user, 
        and a user profile that links the user and dealer objects.
     b) a 'thank you for registering' email is sent to the primary user created for the prospective dealer.
     c) a 'new-registration' event is triggered. 
      
 
"""
__all__ = []

from backends import DealerRegistrationBackend
from forms import DealerRegistrationForm