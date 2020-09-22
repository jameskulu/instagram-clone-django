from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification, name='notification'),
    path('delete/<int:id>', views.delete_notification, name='delete-notification')
]
