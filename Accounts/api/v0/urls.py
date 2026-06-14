from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from . import views



urlpatterns = [
    # register new users 
    path('create-user/', views.register_new_user_api, name='api-create-user'),
    # authenticate users by token auth method in login and logout
    path('api-token-auth-login/', views.custom_login_auth_token, name='api-token-auth'),
    path('api-token-discard-logout/', views.logout_auth_token, name='api-token-discard'),
    # authenticate users by SimpleJWT method in login and logout
    path('api-jwt-login/', views.custom_login_jwt, name='api-jwt-login'),
    path('api-jwt-logout/', views.custom_logout_jwt, name='api-jwt-login'),
    path('api-jwt-refresh/', TokenRefreshView.as_view(), name='jwt-token-refresh'),
    # activation link, resend activation link
    path('activation/<str:token>', views.active_user_registeration_api, name='active-user'),
    path('resend-active-link/', views.resend_activation_link_api, name='active-user'),
    # change password, reset password
    path('change-password/', views.change_password_api, name='change-password'),
    path('reset-password-link/', views.reset_password_link_api, name='reset-password'),
    path('reset-password/<str:token>', views.reset_password_api, name='reset-password'),
]