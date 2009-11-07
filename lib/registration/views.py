"""
Views which allow users to create and activate accounts.

"""

from django.conf import settings
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import login
from django.views.generic.list_detail import object_list
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User

from registration.forms import RegistrationForm, ActivateAndRegisterForm
from registration.models import RegistrationProfile

from django.views.decorators.http import require_POST


def activate_and_register(request, activation_key,
                          form_class=ActivateAndRegisterForm,
                          template_name='registration/activate_and_register.html'):
    activation_key = activation_key.lower() # Normalize before trying anything with it.
    profile = RegistrationProfile.objects.key_valid(activation_key)
    if not profile:
        return render_to_response('registration/key_expired.html',
            context_instance=RequestContext(request)
        )

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=profile.content_object.email,
                password=form.cleaned_data['password1'],
            )
            user.first_name = profile.content_object.first_name
            user.last_name = profile.content_object.last_name
            user.save()
            RegistrationProfile.objects.activate(activation_key)
            user_profile = profile.content_object
            user_profile.user = user
            user_profile.save()
            return redirect('dealer-dashboard')
    else:
        form = form_class()
    return render_to_response(template_name,
                              {  'form': form,
                                 'profile': profile },
                              context_instance=RequestContext(request)
                              )


def register(request, success_url=None,
             form_class=RegistrationForm,
             template_name='registration/registration_form.html',
             extra_context=None):
    """
    Allow a new user to register an account.

    Following successful registration, issue a redirect; by default,
    this will be whatever URL corresponds to the named URL pattern
    ``registration_complete``, which will be
    ``/accounts/register/complete/`` if using the included URLConf. To
    change this, point that named pattern at another URL, or pass your
    preferred URL as the keyword argument ``success_url``.

    By default, ``registration.forms.RegistrationForm`` will be used
    as the registration form; to change this, pass a different form
    class as the ``form_class`` keyword argument. The form class you
    specify must have a method ``save`` which will create and return
    the new ``User``.
    
    By default, use the template
    ``registration/registration_form.html``; to change this, pass the
    name of a template as the keyword argument ``template_name``.
    
    **Required arguments**
    
    None.
    
    **Optional arguments**
    
    ``form_class``
        The form class to use for registration.
    
    ``extra_context``
        A dictionary of variables to add to the template context. Any
        callable object in this dictionary will be called to produce
        the end result which appears in the context.
    
    ``success_url``
        The URL to redirect to on successful registration.
    
    ``template_name``
        A custom template to use.
    
    **Context:**
    
    ``form``
        The registration form.
    
    Any extra variables supplied in the ``extra_context`` argument
    (see above).
    
    **Template:**
    
    registration/registration_form.html or ``template_name`` keyword
    argument.
    
    """
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_user = form.save()
            # success_url needs to be dynamically generated here; setting a
            # a default value using reverse() will cause circular-import
            # problems with the default URLConf for this application, which
            # imports this file.
            return redirect(success_url or 'registration_complete')
    else:
        form = form_class(initial=dict(request.GET.items()))

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(template_name,
                              { 'form': form },
                              context_instance=context)


@permission_required("registration.can_authorize")
def authorized_profiles_list(request):
    return object_list(request,
                       queryset=RegistrationProfile.objects.authorized(),
                       template_name='registration/authorized_list.html',
                       template_object_name='profile')


@permission_required("registration.can_authorize")
def unauthorized_profiles_list(request):
    return object_list(request,
                       queryset=RegistrationProfile.objects.unauthorized(),
                       template_name='registration/unauthorized_list.html',
                       template_object_name='profile')


@require_POST
@permission_required("registration.can_authorize")
def authorize(request, profile_id, email=lambda p: p.content_object.email):
    profile = get_object_or_404(RegistrationProfile, pk=profile_id)
    RegistrationProfile.objects.authorize(profile)
    if email and callable(email):
        RegistrationProfile.objects.send_activation_email(profile, email(profile))
    return redirect('registration_unauthorized')
