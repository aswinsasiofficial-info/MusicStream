from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileUpdateForm


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Account created successfully!')
                return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username or user.email}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


@login_required
def profile(request):
    """User profile view"""
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required
def edit_profile(request):
    """Edit user profile view"""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})
