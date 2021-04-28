from django.shortcuts import render, redirect
from .models import Event, CustomUser
from .forms import EventCreationForm, CustomUserCreationForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth import login, logout


def index(request):
    context = {
        'events': Event.objects.all()
    }
    return render(request, 'events/index.html', context)


def add_event(request):
    if request.method == "POST":
        form = EventCreationForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.owner = request.user
            event.save()
            return redirect('home')
    else:
        form = EventCreationForm()
    return render(request, 'events/add_event.html', {'form': form})

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Success!')
            return redirect('login')
        else:
            messages.error(request, 'Error')
    else:
        form = CustomUserCreationForm()
    return render(request, 'events/register.html', {'form':form})

def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'events/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')