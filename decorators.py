from django.shortcuts import redirect,render
from .models import App

def developer_required(view):
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, "profile") and request.user.profile.role == 'developer':
            return view(request, *args, **kwargs)
        return redirect('home')
    return wrapper
