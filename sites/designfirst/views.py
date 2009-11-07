from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from designfirst import forms


@login_required
def profile_edit(request):
    if request.method == 'POST':
        company_form = forms.CompanyProfileForm(
            request.POST, request.FILES,
            instance=request.user.get_profile().account,
            prefix='company'
        )
        profile_form = forms.UserProfileForm(
            request.POST, request.FILES,
            instance=request.user.get_profile(),
            prefix='profile'
        )

        if company_form.is_valid() and profile_form.is_valid():
            profile = profile_form.save()
            account = company_form.save()
            return redirect('dealer-dashboard')
    else:
        company_form = forms.CompanyProfileForm(
            instance=request.user.get_profile().account,
            prefix='company'
        )
        profile_form = forms.UserProfileForm(
            instance=request.user.get_profile(),
            prefix='profile'
        )

    return render_to_response( 'edit_profile.html', {
        'profile_form': profile_form,
        'company_form': company_form,
    }, context_instance=RequestContext(request))
    
