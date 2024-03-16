from django.urls import path
from .views import admin_sign_up, sign_in
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("auth/login/", sign_in, name="login"),
    path(
        "auth/logout/",
        auth_views.LogoutView.as_view(next_page="/auth/login/"),
        name="logout",
    ),
    path("auth/admin/signup/", admin_sign_up, name="signup"),
]
