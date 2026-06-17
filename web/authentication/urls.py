from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = "authentication"

urlpatterns = [
    # Authentication
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # Profile
    path('profile/', views.user_profile, name='profile'),
    path('edit-profile/', views.user_profile, name='edit_profile'),

    # Password Reset Request
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='authentication/password_reset.html',
            email_template_name='authentication/password_reset_email.html',
            subject_template_name='authentication/password_reset_subject.txt',
            success_url=reverse_lazy('authentication:password_reset_done'),
        ),
        name='password_reset',
    ),

    # Password Reset Email Sent
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='authentication/password_reset_done.html',
        ),
        name='password_reset_done',
    ),

    # Password Reset Confirm
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='authentication/password_reset_confirm.html',
            success_url=reverse_lazy('authentication:password_reset_complete'),
        ),
        name='password_reset_confirm',
    ),

    # Password Reset Complete
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='authentication/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
]