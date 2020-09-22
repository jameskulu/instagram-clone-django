from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login', views.LoginFormView.as_view(), name='login'),
    path('signup', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('email-confirmation', views.email_confirmation, name='email-confirmation'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    # Password
    # path('password-reset/', auth_views.PasswordResetView.as_view(
    #     template_name="Accounts/password/password_reset.html"), name="password_reset"),
    # path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
    #     template_name="Accounts/password/password_reset_done.html"), name="password_reset_done"),
    # path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    #     template_name="Accounts/password/password_reset_confirm.html"), name="password_reset_confirm"),
    # path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
    #     template_name="Accounts/password/password_reset_complete.html"), name="password_reset_complete"),
]
