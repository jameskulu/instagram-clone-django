from django.db import models
from django.contrib.auth.models import User
import os
from Users.models import Profile
from django.core.exceptions import ValidationError


class Tag(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


def file_size(value):
    pass
    # limit = 100 * 1024 * 1024
    # if value.size > limit:
    #     raise ValidationError(
    #         'File too large. Size should not exceed 100 MiB.')


class Post(models.Model):
    caption = models.TextField(max_length=500)
    file = models.FileField(upload_to='files', null=True,
                            blank=True, validators=[file_size])
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    dislikes = models.ManyToManyField(
        User, related_name='dislikes', blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tag = models.ManyToManyField(
        Tag, related_name='tag', blank=True)
    archive = models.BooleanField(default=False)
    save_post = models.ManyToManyField(
        User, related_name='save_post', blank=True)

    def __str__(self):
        return self.caption

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension


class Comment(models.Model):
    content = models.CharField(max_length=160)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
