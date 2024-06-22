from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):

    body = forms.CharField(
        label = '',
        widget=forms.Textarea(attrs={
            'rows': '3',
            'placeholder': 'Tell your community about it...'
        })
    )

    class Meta:
        model = Post
        fields = ['body']


class CommentForm(forms.ModelForm):

    comment = forms.CharField(
        label = '',
        widget=forms.Textarea(attrs={
            'rows': '3',
            'placeholder': 'Comment on this post...'
        })
    )

    class Meta:
        model = Comment
        fields = ['comment']