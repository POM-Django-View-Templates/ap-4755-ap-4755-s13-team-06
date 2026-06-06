from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

from .models import CustomUser


def register_view(request):
    user = CustomUser.objects.create(
        email="new_user@mail.com",
        first_name="New",
        last_name="User",
        middle_name="Middle",
        role=0,
        is_active=True
    )

    user.set_password("12345")
    user.save()

    return HttpResponse("User registered")


def login_view(request):
    user = authenticate(
        request,
        username="new_user@mail.com",
        password="12345"
    )

    if user is not None:
        login(request, user)
        return HttpResponse("User logged in")

    return HttpResponse("Invalid credentials")


def logout_view(request):
    logout(request)
    return HttpResponse("User logged out")
