from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("post-details/<slug:slug>/", views.post_details, name="post_details"),
]