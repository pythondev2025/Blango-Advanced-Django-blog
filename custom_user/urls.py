from django.urls import path, include
from . import views


urlpatterns = [
    path("delete_unwanted/", views.delete_unwanted_users, name="delete_users"),
]
