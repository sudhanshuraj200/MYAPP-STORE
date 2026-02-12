from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile, App, Review
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .decorators import developer_required

# Create your views here.

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        if not username or not password:
            return render(request, 'auth/register_user.html', {'error': 'Username and password are required.'})
        try:
            user = User.objects.create_user(username=username, password=password)
            Profile.objects.update_or_create(user=user, defaults={'role': 'user'})
        except IntegrityError:
            return render(request, 'auth/register_user.html', {'error': 'Username already exists.'})
        return redirect(f"{reverse('login')}?role=user")
    return render(request, 'auth/register_user.html')


def register_developer(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        if not username or not password:
            return render(request, 'auth/register_developer.html', {'error': 'Username and password are required.'})
        try:
            user = User.objects.create_user(username=username, password=password)
            Profile.objects.update_or_create(user=user, defaults={'role': 'developer'})
        except IntegrityError:
            return render(request, 'auth/register_developer.html', {'error': 'Username already exists.'})
        return redirect(f"{reverse('login')}?role=developer")
    return render(request, 'auth/register_developer.html')


def login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next') or 'home'
    selected_role = (request.POST.get('role') or request.GET.get('role') or 'user').strip()
    if request.method == 'POST':
        role = selected_role
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        if not username or not password:
            return render(request, 'auth/login.html', {'error': 'Username and password are required.', 'selected_role': selected_role})
        user = authenticate(username=username, password=password)
        if user:
            Profile.objects.update_or_create(user=user, defaults={'role': role})
            login(request, user)
            return redirect(next_url)
        if not User.objects.filter(username=username).exists():
            if role == 'developer':
                return redirect('register_developer')
            return redirect('register_user')
        return render(request, 'auth/login.html', {'error': 'Invalid username or password.', 'selected_role': selected_role})
    return render(request, 'auth/login.html', {'selected_role': selected_role})


@login_required
@developer_required
def upload_app(request):
    if request.method == 'POST':
        if 'apk_file' not in request.FILES:
            return render(request, 'developer/upload.html', {'error': 'APK file is required.'})
        App.objects.create(
            developer=request.user,
            name=request.POST['name'],
            description=request.POST['description'],
            category=request.POST['category'],
            version=request.POST['version'],
            image=request.FILES.get('image'),
            apk_file=request.FILES['apk_file']
        )
        return redirect('home')
    return render(request, 'developer/upload.html')


#

def home(request):
    apps = App.objects.filter(status='Approved')
    return render(request, 'apps/home.html', {'apps': apps})


def search(request):
    q = (request.GET.get('q') or '').strip()
    if q:
        apps = App.objects.filter(name__icontains=q, status='Approved')
    else:
        apps = App.objects.none()
    return render(request, 'apps/search.html', {'apps': apps, 'q': q})

@login_required
def download_app(request, id):
    app = get_object_or_404(App, id=id, status='Approved')
    app.downloads += 1
    app.save()
    return redirect(app.apk_file.url)


@login_required
def add_review(request, id):
    if request.method != 'POST':
        return redirect('app_detail', id=id)
    app = get_object_or_404(App, id=id)
    Review.objects.create(
        app=app,
        user=request.user,
        rating=request.POST.get('rating', ''),
        comment=request.POST.get('comment', '').strip()
    )
    return redirect('app_detail', id=id)


def app_detail(request, id):
    app = get_object_or_404(App, id=id, status='Approved')
    return render(request, 'apps/app_detail.html', {'app': app})


@login_required
@developer_required
def delete_app(request, id):
    app = get_object_or_404(App, id=id, developer=request.user)
    if request.method == 'POST':
        app.delete()
        return redirect('home')
    return redirect('app_detail', id=id)


def logout_view(request):
    logout(request)
    return redirect('home')
