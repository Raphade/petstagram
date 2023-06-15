from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    # description = forms.TextInput()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # def __init__(self, user, *args, **kwargs):
    #     self.user = user
    #     super(UserCreationForm, self).__init__(*args, **kwargs)

class ProfileUpdateForm(forms.ModelForm):
        
    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'form-control mb-3 file-input',
        'id': 'upload-box-profile-pic',
        'accept':'image/*',
        'onchange': 'previewImageProfile(event)',
        'style': 'position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0; cursor: pointer;',
        'placeholder': 'Image',
    }))

    class Meta:
        model = Profile
        fields = ['profile_picture']