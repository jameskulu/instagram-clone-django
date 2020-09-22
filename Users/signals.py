from django.db.models.signals import post_save, m2m_changed
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from Post.models import Post, Comment
from Notification.models import Notification
from datetime import datetime
from django.db.models import Q


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.userprofile.save()


@receiver(m2m_changed, sender=Profile.following.through)
def add_follower(sender, instance,  action, pk_set, reverse, **kwargs):
    followed_users = []
    logged = User.objects.get(userprofile=instance)
    loggedUser = User.objects.get(username=logged)
    for i in pk_set:
        user = User.objects.get(pk=i)
        following_obj = Profile.objects.get(user=user)
        followed_users.append(following_obj)

    if action == 'pre_add':
        for i in followed_users:
            print(i.user)
            notify = Notification.objects.create(
                sender=loggedUser, receiver=User.objects.get(username=i.user), notification_type='follow')
            i.follower.add(logged)
            i.save()

    if action == 'pre_remove':
        for i in followed_users:
            notify = Notification.objects.filter(
                sender=loggedUser, receiver=User.objects.get(username=i.user), notification_type='follow')
            if notify.exists():
                notify.delete()
            i.follower.remove(logged)
            i.save()


@receiver(m2m_changed, sender=Post.likes.through)
def like_notification(sender, instance,  action, pk_set, reverse, **kwargs):
    liked_users = []
    for i in pk_set:
        user = User.objects.get(pk=i)
        following_obj = Profile.objects.get(user=user)
        liked_users.append(following_obj)
    if action == 'pre_add':
        for i in liked_users:
            if User.objects.get(username=i.user) != instance.user.user:
                notify = Notification.objects.create(
                    sender=User.objects.get(username=i.user), receiver=instance.user.user, notification_type='like', post=instance)

            if User.objects.get(username=i.user) in instance.dislikes.all():
                instance.dislikes.remove(
                    User.objects.get(username=i.user))

    if action == 'pre_remove':
        for i in liked_users:
            if User.objects.get(username=i.user) != instance.user.user:
                notify = Notification.objects.filter(
                    sender=User.objects.get(username=i.user), receiver=instance.user.user, notification_type='like', post=instance)
                if notify.exists():
                    notify.delete()


@receiver(m2m_changed, sender=Post.dislikes.through)
def dislike_notification(sender, instance,  action, pk_set, reverse, **kwargs):
    liked_users = []
    for i in pk_set:
        user = User.objects.get(pk=i)
        following_obj = Profile.objects.get(user=user)
        liked_users.append(following_obj)
    if action == 'pre_add':
        for i in liked_users:
            if User.objects.get(username=i.user) in instance.likes.all():
                instance.likes.remove(
                    User.objects.get(username=i.user))


@receiver(post_save, sender=Comment)
def comment_notification(sender, instance, created, **kwargs):
    if created:
        if instance.user != instance.post.user.user:
            Notification.objects.create(
                sender=instance.user, receiver=instance.post.user.user, notification_type='comment', post=instance.post, preview=instance.content)
