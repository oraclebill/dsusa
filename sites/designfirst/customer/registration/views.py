from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from registration.models import RegistrationProfile
from registration.backends import get_backend


def setup_and_activate(request, activation_key, backend,
                       form_class=UserCreationForm,
                       template_name='registration/setup_new_user.html',
                       fail_template_name='registration/activate.html',
                       success_url=None):

    backend = get_backend(backend)
    profile = get_object_or_404(RegistrationProfile, activation_key=activation_key)
    if not backend.can_activate(activation_key):
        return render_to_response(fail_template_name,
                                  context_instance=RequestContext(request))

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=profile.user)
        if form.is_valid():
            form.save()
            account = backend.activate(request, activation_key)
            if success_url:
                return redirect(success_url)
            to, args, kwargs = backend.post_activation_redirect(request, account)
            return redirect(to, *args, **kwargs)
    else:
        # do not prepopulate form with generated user data
        form = form_class()

    return render_to_response(template_name, {'form': form},
                              context_instance=RequestContext(request))
