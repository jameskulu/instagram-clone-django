from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('likes', views.likes, name='likes'),
    path('dislikes', views.dislikes, name='dislikes'),
    path('upload', views.upload, name='upload'),
    path('tags/<str:tag_slug>', views.tag_page, name='tag'),
    path('<int:pk>', views.detail, name='detail'),
    path('comment/<int:pk>', views.comment, name='comment'),
    path('<int:pk>/update', views.update, name='update'),
    path('<int:pk>/delete', views.delete, name='delete'),
    path('comment/<int:pk>/delete', views.delete_comment, name='delete-comment'),
    path('search', views.search, name='search'),
    path('save/<int:pk>', views.save, name='save')
]
