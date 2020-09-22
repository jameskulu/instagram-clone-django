from django.shortcuts import render, redirect

# imports for Signup
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from .decoraters import unauthenticated_user
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponseRedirect
from django.urls import reverse

# imports for login
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.utils.decorators import method_decorator

# imports for logout
from django.contrib.auth.decorators import login_required


@unauthenticated_user
def signup(request):

    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            request.session['emailConfirm'] = form.cleaned_data.get('email')
            current_site = get_current_site(request)

            # For Email Confirmation
            mail_subject = 'Activate your Jistagram account.'
            message = render_to_string('Accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponseRedirect(reverse('email-confirmation'))

    return render(request, 'Accounts/signup1.html', {'form': form})


@method_decorator(unauthenticated_user, name='dispatch')
class LoginFormView(SuccessMessageMixin, LoginView):
    template_name = 'Accounts/login1.html'
    success_url = 'home'
    redirect_authenticated_user = False
    success_message = "You were successfully logged in."


@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, 'You have successfully logged out')
    # return redirect('home')
    return HttpResponseRedirect(request.GET.get('next', '/'))


@unauthenticated_user
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.userprofile.email_confirmed = True
        user.save()
        auth.login(request, user,
                   backend='django.contrib.auth.backends.ModelBackend')
        messages.success(
            request, f'Welcome {user.first_name} ! You have successfully verified your account.')
        return redirect('home')
    else:
        messages.warning(request, 'Activation link is invalid!')
        return redirect('home')


@unauthenticated_user
def email_confirmation(request):
    email = request.session['emailConfirm']
    return render(request, 'Accounts/email_confirmation.html', {'email': email})
