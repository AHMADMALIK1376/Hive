from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm, ProfileUpdateForm
from posts.models import Post

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to Hive, {user.username}! 🐝')
            return redirect('feed')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    # We'll use Django's built-in LoginView — just render the template
    return render(request, 'core/login.html')

@login_required
def feed_view(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'core/feed.html', {'posts': posts})

@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.posts.all().order_by('-created_at')

    if request.method == 'POST' and request.user == user:
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile', username=username)
    else:
        form = ProfileUpdateForm(instance=user.profile) if request.user == user else None

    context = {
        'profile_user': user,
        'posts': posts,
        'form': form,
        'followers_count': user.followers.count(),
        'following_count': user.following.count(),
    }
    return render(request, 'core/profile.html', context)

@login_required
def search_view(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=query) if query else []
    return render(request, 'core/search.html', {'users': users, 'query': query})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')