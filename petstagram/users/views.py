from django.shortcuts import redirect, render
from .forms import UserRegisterForm
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account for {username} has been created!')
            return redirect('#')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})