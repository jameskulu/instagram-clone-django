from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    tag = forms.CharField(
        label='Tags (Enter comma seperated value)', max_length=100, required=False)

    class Meta:
        model = Post
        fields = ['caption', 'file', 'tag']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
