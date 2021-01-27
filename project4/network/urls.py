from django.urls import path
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API Routes
    path("post", views.new_post, name="new post"),
    path("profile/<username>", views.profile_page, name="profile page"),
    path("following", views.following_posts, name="following posts"),
    path("edit", views.edit, name="edit"),
    path("like", views.like, name="like"),
]
