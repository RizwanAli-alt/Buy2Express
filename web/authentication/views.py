from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserProfileForm


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()              # password is hashed inside form.save()
            login(request, user)            # auto login after signup
            messages.success(request, f"Welcome to Buy2Express, {user.username}!")
            return redirect('home')
        # form errors will be passed to template automatically
    else:
        form = UserRegistrationForm()
    return render(request, 'authentication/register.html', {'form': form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')  # already logged in, go home

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, "Please enter both username and password.")
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                next_url = request.GET.get('next', reverse('home'))
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password. Please try again.")

    return render(request, 'authentication/login.html')


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('authentication:login')


@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('authentication:profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'authentication/profile.html', {'form': form})
