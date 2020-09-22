from django.db import models
from Post.models import Post
from django.contrib.auth.models import User


NOTIFICATION_TYPE = (
    ('like', 'like'),
    ('follow', 'follow'),
    ('comment', 'comment')
)


class Notification(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='receiver')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='post', blank=True, null=True)
    is_read = models.BooleanField(default=False)
    preview = models.CharField(max_length=200, blank=True, null=True)
    notification_type = models.CharField(
        choices=NOTIFICATION_TYPE, max_length=7)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
