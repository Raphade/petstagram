from django import forms

from .models import Post, Comment


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
        'accept': 'image/*',
        'onchange': 'previewImage(event)',
        'style': '',
        'placeholder': 'Image',
        'accept': 'image/*',
    }))

    class Meta:
        model = Post
        fields = ('description', 'media')


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Add a comment...',
        'required': 'true',
        'class': 'mdl-comment-input',
        'row': '5',
        'cols': '40',
    }))

    class Meta:
        model = Comment
        fields = ['text']
