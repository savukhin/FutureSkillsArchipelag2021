from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser, CustomAdmin
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .tokens import account_activation_token
from django.views import View
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseNotFound, HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


@user_passes_test(lambda user: not user.is_authenticated, login_url='/')
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            newCustomUser = CustomUser(user=form.instance)
            newCustomUser.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)
            return redirect('/')
        return render(request, template_name='register.html', context={'form': form})

    return render(request, template_name='registration.html')


@user_passes_test(lambda user: not user.is_authenticated, login_url='/')
def loginView(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if not user:
            return render(request, template_name='login.html',
                          context={"errors": "User or password is not correct!"})

        login(request, user)
        return redirect('/')

    return render(request, template_name='login.html')


@login_required(redirect_field_name='/')
def logoutView(request):
    logout(request)
    return redirect('/')


class NewPassword(View):
    def get_user(self, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        return user

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64, token)

        if user is not None and account_activation_token.check_token(user, token):
            return render(request, 'newPassword.html')
        else:
            return HttpResponseNotFound('<h1>Page not found</h1>')

    def post(self, request, uidb64, token):
        user = self.get_user(uidb64, token)
        if user is not None and account_activation_token.check_token(user, token):
            if request.POST['password1'] != request.POST['password2']:
                return render(request, template_name='newPassword.html', context={'errors': 'passwords are not equal'})
            user.set_password(request.POST['password1'])
            user.save()
            return redirect('/')
        else:
            return HttpResponseNotFound('<h1>Page not found</h1>')


@user_passes_test(lambda user: not user.is_authenticated, login_url='/')
def forgot_password(request):
    if request.method == 'POST':
        users = User.objects.filter(username=request.POST['username'], email=request.POST['email'])
        if len(users) == 0:
            return render(request, template_name='forgotPassword.html', context={'errors': 'User does not exists!'})
        elif len(users) > 1:
            return render(request, template_name='forgotPassword.html', context={'errors': 'User more than one!'})
        else:
            token = account_activation_token.make_token(users[0])
            print(token)
            print(users[0].id)
            return redirect('/newPassword/' + urlsafe_base64_encode(force_bytes(users[0].id)) + "/" + token)

    return render(request, template_name='forgotPassword.html')
