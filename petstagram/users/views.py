from django.shortcuts import redirect, render
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.shortcuts import render
from .forms import ProfileUpdateForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            new_user = form.save()
            print("new_user:\t", new_user)
            profile = Profile(user=new_user)
            profile.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account for {username} has been created!')
            return redirect('posts-home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            return redirect('profile')
    else:
        p_form = ProfileUpdateForm()


    return render(request, 'users/profile.html', {'form': p_form, 'title': 'Profile'})
