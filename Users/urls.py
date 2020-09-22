from django.urls import path
from . import views


urlpatterns = [
    path('profile/<username>', views.profile, name="profile"),
    path('follow-unfollow', views.follow_unfollow, name='follow-unfollow'),
    path('edit-profile', views.edit_profile, name='edit-profile'),
    path('archive', views.archive, name='archive'),
    path('archive_toggle/<int:pk>', views.archive_toggle, name='archive-toggle'),
    path('save_posts', views.save_posts, name='save-posts'),
    path('change-password', views.change_password, name="change-password"),
]
