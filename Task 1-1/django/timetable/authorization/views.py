from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login
from .models import CustomUser, CustomAdmin

# Create your views here.


def register(request):
    print(request.method)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print("OK")
        if form.is_valid():
            print("VALID")
            form.save()
            newCustomUser = CustomUser(user=form.instance)
            newCustomUser.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)
            return redirect('/')
        return render(request, template_name='register.html', context={'form': form})

    return render(request, template_name='register.html')