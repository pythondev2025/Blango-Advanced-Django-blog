from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import User


@login_required
def profile(request):
    return render(request, "custom_user/profile.html")


@login_required
def delete_unwanted_users(request):
    if request.user.is_active and request.user.is_superuser:
        del_users = User.objects.filter(
            is_active=False
            ).delete()    # date_joined__lt=timezone.now() - timedelta(days=1
        return HttpResponse(f"successfully deleted {del_users[0]} inactive users.")
    else:
        raise PermissionDenied("Permission Denied. You are Unable to access this page.")