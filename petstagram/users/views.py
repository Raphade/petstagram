from django.shortcuts import redirect, render
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.models import Profile


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
    return render(request, 'users/profile.html')
