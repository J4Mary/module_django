from django.contrib.auth import login
from django.contrib.auth import logout as logout_

from django.shortcuts import render, redirect
from users.forms import RegisterForm, UserInfo
from users.models import User


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data.get('username'),
                email=form.cleaned_data.get('email'),
            )
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            login(request, user)
            return redirect('/')
    return render(request, 'users/register.html', {'form': form})


def logout(request):
    logout_(request)
    return redirect('/')


def user_info(request):
    form = UserInfo()
    return render(request, 'users/personal_page.html', {'form': form})
