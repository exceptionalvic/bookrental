from django.urls import path
from .views import admin_sign_up, sign_in
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('auth/login/', sign_in, name='login'),
    path('auth/logout/', auth_views.LogoutView.as_view(next_page="/"), name='logout'),
    
    path('auth/admin/signup/', admin_sign_up, name='signup'),
    
    # path('auth/login/', LoginView, name='login'),
    # path('auth/signup/', signupview, name='signup_view'),
    # path('auth/view/', authview, name='authview'),
    # path('auth/login/session-continue/', after_login, name='continue_login'),
    # # password reset
    # path('auth/password-reset/', PasswordResetView, name='password_reset'),
    # path('auth/password-reset/otp/', PasswordOTPView, name='password_reset_otp'),
    # path('auth/password-reset/otp/confirm/', PasswordOTPConfirmationView, name='password_reset_otp_confirmation'),
    # path('auth/password-change/', ChangePasswordView, name='change_password'),
    
]