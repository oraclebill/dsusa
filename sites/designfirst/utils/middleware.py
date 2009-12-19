from django.core.urlresolvers import reverse
from django.http import HttpResponseNotAllowed, HttpResponseRedirect

from customer.models import Dealer

## some site specific middleware

class UserAccountMiddleware(object):
    """
    Create an 'account' property on request for logged in customers, and fail 
    if logged in user has no account and is not 'staff'.
    """    
    def process_request(self, request):
        # if not logged in user, quit 
        user = getattr(request, 'user', None)
        if not user or user.is_anonymous():
            return None
        # if valid customer, add account to request, and quit 
        try:
            request.account = user.get_profile().account
            assert(request.account)
            
            if request.account.status != Dealer.Const.ACTIVE:
            	request.session.flush()
                if request.account.status ==  Dealer.Const.SUSPENDED:
                    return HttpResponseRedirect(reverse('account-suspended'))
                else: 
                    return HttpResponseRedirect(reverse('account-inactive'))
        except:
            # if no profile, must be staff user, right?
            if not user.is_staff: 
                return HttpResponseNotAllowed('invalid login. please contact support.')
            request.account = None
        # user is staff, return 'OK to proceed'...
        return None
    
    
