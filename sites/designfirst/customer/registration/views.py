from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext


def setup_new_user(request, username, form_class=UserCreationForm,
                       template_name='registration/setup_new_user.html',
                       post_save_redirect='dealer-dashboard'):
    user = get_object_or_404(User, username=username)

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect(post_save_redirect)
    else:
        # do not prepopulate form with generated user data
        form = form_class()

    return render_to_response(template_name, {'form': form},
                              context_instance=RequestContext(request))



