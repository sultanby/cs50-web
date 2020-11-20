from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.core.paginator import Paginator

from .models import User, Post, ProfileFollows


def index(request):
    # Get all the posts
    all_posts = Post.objects.order_by("-post_time").all()

    # Separating all the posts to the groups of 10
    paginator = Paginator(all_posts, 10)


    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.user.is_authenticated:
        return render(request, "network/index.html", {
            'all_posts': all_posts,
            'page_obj': page_obj,

        })

    else:
        return HttpResponseRedirect(reverse("login"))



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
@login_required
def new_post(request):
    # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check if post is not empty
    new_post_data = json.loads(request.body)
    new_post_text = new_post_data.get("new_post_text")

    # Get contents of new post
    post_text = new_post_data.get("new_post_text", "")

    if new_post_text == [""]:
        return JsonResponse({
            "error": "Can't submit empty text area"
        }, status=400)

    # Add post to db
    add_new_post_to_db = Post(
        user_posted=request.user,
        post=post_text,
    )
    add_new_post_to_db.save()

    return JsonResponse({"message": "Post added successfully."}, status=201)

@csrf_exempt
@login_required
def profile_page(request, username):
    user = User.objects.get(username=username)
    all_users_posts = Post.objects.filter(user_posted=user).order_by("-post_time")
    followings = user.following_user.all()
    followers = user.follower_user.all()

    paginator = Paginator(all_users_posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.user.is_authenticated:
        return render(request, "network/profile.html", {
        'all_posts': all_users_posts,
        'page_obj': page_obj,
        'username': username,
        'followers': followers,
        'followings': followings,
    })

    else:
        return HttpResponseRedirect(reverse("login"))