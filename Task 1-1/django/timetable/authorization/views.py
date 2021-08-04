from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login
from .models import CustomUser, CustomAdmin
from django.contrib.auth.models import User

# Create your views here.


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


def loginView(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if not user:
            return render(request, template_name='login.html',
                          context={"errors": "User or password is not correct!"})

        login(request, user)
        return redirect('/')

    return render(request, template_name='login.html')


def forgot_password(request):
    if request.method == 'POST':
        users = User.objects.filter(username=request.POST['username'], email=request.POST['email'])
        if len(users) == 0:
            return render(request, template_name='forgotPassword.html', context={'errors': 'User does not exists!'})
        elif len(users) > 1:
            return render(request, template_name='forgotPassword.html', context={'errors': 'User more than one!'})
        else:
            return redirect('/')

    return render(request, template_name='forgotPassword.html')
