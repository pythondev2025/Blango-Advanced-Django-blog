from django.urls import path
from . import api_views


urlpatterns = [
    path("posts/", api_views.post_list, name="api_post_list"),
    path("posts/<int:pk>/", api_views.post_details, name="api_post_details")
]