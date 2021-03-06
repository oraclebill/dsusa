from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import backends
from django.contrib.auth import models as auth_models
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
import models


class DealerBackend(backends.ModelBackend):
    """
    Checks that user's dealer is active.
    """
    def authenticate(self, username=None, password=None):
        try:
            user = auth_models.User.objects.get(username=username)
            if user.check_password(password):
#                if not user.is_staff and user.get_profile().account.status \
#                        in (models.Dealer.Const.PENDING, models.Dealer.Const.ARCHIVED):
#                    return None
                return user
        except ObjectDoesNotExist:
            return None    
