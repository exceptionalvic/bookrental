from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
    HttpResponseRedirect,
    HttpResponse,
)
from django.contrib import messages
from django.urls import reverse, reverse_lazy
import json
import time
from itertools import chain
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login, authenticate
import base64
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login

# from users.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.generic import View
from . import forms


User = get_user_model()


def admin_sign_up(request):
    """Signup admin user"""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        if email and password:
            try:
                get_user = User.objects.get(email=email)
                if get_user:
                    messages.error(
                        request, "User with that email already exists"
                    )
                    return redirect("users:signup")

            except User.DoesNotExist:
                # password validation
                try:
                    is_valid_password = validate_password(password)
                except Exception as validation_error:
                    messages.error(request, str(validation_error))
                    return redirect("users:signup")
                # print(is_valid_password)
                if is_valid_password is None:
                    user = User.objects.create_user(
                        email=email, password=password,
                        is_staff=True,
                        is_superuser=True
                    )
                    user.save()
                    login(
                        request,
                        user,
                        backend="django.contrib.auth.backends.ModelBackend",
                    )
                    if user.is_staff:
                        return redirect("core:admin-dashboard")
                    else:
                        return redirect("core:user-dashboard")
        else:
            messages.error(
                request, "Did you forget to input email or password?"
            )
            return redirect("users:signup")
    context = {
        # 'form' : form
    }
    return render(request, "users/signup.html", context)


def sign_in(request):
    """Sign in a user or admin"""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = authenticate(email=email, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    if user.is_staff:
                        return redirect("core:admin-dashboard")
                    else:
                        return redirect("core:user-dashboard")
                else:
                    messages.error(
                        request, f"Inactive account. Reach admin for help"
                    )
                    return redirect("users:login")
            else:
                messages.error(request, f"Invalid login credentials")
                return redirect("users:login")

        except User.DoesNotExist:
            messages.error(
                request, "User does not exist. Do you want to register?"
            )
            return redirect("users:login")

    context = {}
    return render(request, "users/login.html", context)
