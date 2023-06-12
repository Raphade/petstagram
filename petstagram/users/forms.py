from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    # description = forms.TextInput()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # def __init__(self, user, *args, **kwargs):
    #     self.user = user
    #     super(UserCreationForm, self).__init__(*args, **kwargs)