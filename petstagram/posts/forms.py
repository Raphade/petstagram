from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control mb-3',
        'style': '',
        'placeholder': 'Description',
        'rows': '4',
    }))

    media = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'form-control mb-3 file-input',
        'id': 'image-upload',
        'accept':'image/*',
        'onchange': 'previewImage(event)',
        'style': '',
        'placeholder': 'Image',
        'accept': 'image/*',
    }))

    class Meta:
        model = Post
        fields = ('description', 'media')
