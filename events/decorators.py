from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def owner_required(view_func, event):
    def wrapper_func(request, *args, **kwargs):
        if request.user != event.owner:
            return HttpResponse('You are not authorized for editing this page')
        else:
            return view_func(request, *args, **kwargs)
        return wrapper_func
