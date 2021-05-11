from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, ListView

from .models import Event, CustomUser
from .forms import EventCreationForm, CustomUserCreationForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import login, logout
from .decorators import unauthenticated_user


class HomeView(ListView):
    model = Event
    template_name = 'events/index.html'
    context_object_name = 'events'
    paginate_by = 3


class MyEventsView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events/my_events.html'
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        events = Event.objects.filter(visitors__id=request.user.id)
        return render(request, self.template_name, {'events': events})


class Profile(DetailView):
    template_name = 'events/user_profile.html'

    queryset = CustomUser.objects.all()

    def get_object(self):
        username = self.kwargs.get("username")
        return get_object_or_404(CustomUser, username=username)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = Event.objects.filter(owner__username=context['object'].username)
        return context


@unauthenticated_user
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You are now able to log in')
            return redirect('login')
        else:
            messages.error(request, 'Error')
    else:
        form = CustomUserCreationForm()
    return render(request, 'events/register.html', {'form': form})


@login_required(login_url='login')
def edit_profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile', request.user.username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'events/edit_profile.html', context)


@unauthenticated_user
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


def view_event(request, event_id):
    event_item = get_object_or_404(Event, pk=event_id)
    if request.user in event_item.visitors.all():
        signup = True
    else:
        signup = False
    if request.method == "POST":
        if request.POST['signup'] == 'OK':
            event_item.visitors.add(request.user)
            print(request.POST)
            messages.success(request, 'Success!')
            return redirect(event_item.get_absolute_url())
        elif request.POST['signup'] == 'NEOK':
            messages.error(request, 'You are not authorized!')
            return redirect('login')
        else:
            event_item.visitors.remove(request.user)
            return redirect(event_item.get_absolute_url())
    return render(request, 'events/view_event.html', {
        'item': event_item,
        'signup': signup
    })


@login_required(login_url='login')
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


@login_required(login_url='login')
def edit_event(request, event_id):
    event_item = get_object_or_404(Event, pk=event_id)
    if request.user == event_item.owner:
        if request.method == "POST":
            form = EventCreationForm(request.POST, instance=event_item)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your event has been updated!')
                return redirect('view_event', event_item.pk)
        else:
            form = EventCreationForm(instance=event_item)
    else:
        return redirect('home')
    context = {
        'form': form,
    }
    return render(request, 'events/edit_event.html', context)
