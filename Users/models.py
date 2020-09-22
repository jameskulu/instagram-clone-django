from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='userprofile')
    image = models.ImageField(default="default.jpg",
                              upload_to='profile-picture')
    following = models.ManyToManyField(
        User, related_name='following', blank=True)
    follower = models.ManyToManyField(
        User, related_name='follower', blank=True)
    bio = models.CharField(max_length=100, blank=True)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"
