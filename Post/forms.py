from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    tag = forms.CharField(
        label='Tags (Enter comma seperated value)', max_length=100, required=False)
    file = forms.FileField(widget=forms.FileInput(
        attrs={'accept': 'image/*,video/*'}))

    class Meta:
        model = Post
        fields = ['caption', 'file', 'tag']

    # def clean_file(self):
    #     file = self.cleaned_data.get('file')
    #     limit = 100 * 1024 * 1024
    #     if file.size > limit:
    #         raise forms.ValidationError(
    #             'File too large. Size should not exceed 100 MiB.')
    #     return file


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
