"""blango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django_registration.backends.activation.views import RegistrationView
from custom_user.forms import CustomRegistrationForm
from custom_user import views
import debug_toolbar


urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        "accounts/register/", 
        RegistrationView.as_view(form_class=CustomRegistrationForm),
        name="django_registration_register",
    ),
    path("", include("blog.urls")),
    path("accounts/", include("django_registration.backends.activation.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("allauth.urls")),
    path("accounts/profile/", views.profile, name="profile"),
    path("users/", include("custom_user.urls")),
    path("api/v1/", include("blog.api_urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls))
    ]
