from django.shortcuts import render, redirect
from .models import Notification


def notification(request):
    notification = Notification.objects.filter(
        receiver=request.user).order_by('-created')
    Notification.objects.filter(
        receiver=request.user, is_read=False).update(is_read=True)
    context = {
        'notification': notification
    }
    return render(request, 'Notification/notification.html', context)


def notification_count(request):
    notification_count = 0
    if request.user.is_authenticated:
        notification_count = Notification.objects.filter(
            receiver=request.user, is_read=False)
    return {'notification_count': notification_count}


def delete_notification(request, id):
    notify = Notification.objects.get(id=id)
    notify.delete()
    return redirect('notification')
