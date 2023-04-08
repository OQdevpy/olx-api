from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required

from .models import Account


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/profile/logout')
    form = AuthenticationForm(request)
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('/profile/logout')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            login(request, user)
            print(form.data.get('role'))
            Account .objects.create(
                account=user,
                role=form.data.get('role'),
            )
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)
