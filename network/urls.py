
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path("profile/<str:username>", views.user_profile, name="user_profile"),
    path("api", views.api, name="api"),
    path("api/<str:username>", views.api_usr, name="api_usr"),
    path("api/interaction/<str:post_id>", views.interaction, name="interaction"),
    path("discover", views.discover, name="discover"),
    path("edit/<str:post_id>", views.edit_post, name="edit_post")
]
