from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import User, Post, ProfileFollows


def index(request):
    # Get all the posts
    all_posts = Post.objects.order_by("-post_time").all()

    # Separating all the posts to the groups of 10
    paginator = Paginator(all_posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_obj = add_pic_to_post(page_obj)
    if request.user.is_authenticated:
        return render(request, "network/index.html", {
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
            }, status=403)
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
        file = request.FILES["profile_pic"]
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, profile_pic=file)
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

    new_post_text = request.POST.get("new_post_text")

    if (new_post_text=="" or new_post_text==None):
        return JsonResponse({
            "error": "Can't submit empty text area"
        }, status=400)

    # Add post to db
    add_new_post_to_db = Post(
        user_posted=request.user,
        post=new_post_text,
    )
    add_new_post_to_db.save()

    return JsonResponse({"message": "Post added successfully."}, status=201)


@csrf_exempt
@login_required
def profile_page(request, username):
    # get the user which profile is currently opened
    users_profile = User.objects.get(username=username)

    # make sure if logged in user is following users_profile
    is_followed = ProfileFollows.objects.filter(user_to_follow=users_profile.id, follower=request.user).exists()

    # get all users_profile posts in reverse chronological order
    all_users_posts = Post.objects.filter(user_posted=users_profile).order_by("-post_time")
    followers = users_profile.following_user.all()
    followings = users_profile.follower_user.all()

    # add paginator
    paginator = Paginator(all_users_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_obj = add_pic_to_post(page_obj)
    # add or delete follower from db
    if request.method == "POST":
        if "unfollow_btn" in request.POST:
            ProfileFollows.objects.get(user_to_follow=users_profile, follower=request.user).delete()
        elif "follow_btn" in request.POST:
            ProfileFollows.objects.create(user_to_follow=users_profile, follower=request.user)
        else:
            print("Error: wrong input name")
        return HttpResponseRedirect(reverse("profile page", args=(username,)))

    return render(request, "network/profile.html", {
        'page_obj': page_obj,
        'username': username,
        'followers': followers,
        'followings': followings,
        'is_followed': is_followed,
        'users_profile': users_profile
    })


@csrf_exempt
@login_required
def following_posts(request):
    # Get all the following posts
    user = request.user
    all_follows = ProfileFollows.objects.filter(follower=user)
    all_posts = Post.objects.filter(user_posted__id__in=all_follows.values("user_to_follow_id")).order_by("-post_time")

    # Separating all the posts to the groups of 10
    paginator = Paginator(all_posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    page_obj = add_pic_to_post(page_obj)

    if request.user.is_authenticated:
        return render(request, "network/index.html", {
            'page_obj': page_obj,
        })
    else:
        return HttpResponseRedirect(reverse("login"))


def add_pic_to_post(posts):
    for post in posts:
        user_posted_username = post.user_posted
        user = User.objects.get(username=user_posted_username)
        post.profile_pic = user.profile_pic
    return posts

@csrf_exempt
@login_required
def edit(request):
    if request.method == "POST":
        post_id = request.POST.get('id')
        new_post_text = request.POST.get('editedPostText')

        post = Post.objects.get(id=post_id)
        if post.user_posted == request.user:
            post.post = new_post_text
            post.save()
            return JsonResponse({"message": "Post added successfully."}, status=201)
        else:
            return JsonResponse({"error": "can't edit"}, status=400)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)

@csrf_exempt
@login_required
def like(request):
    if request.method == "POST":
        post_id = request.POST.get('id')
        user = request.user
        post = Post.objects.get(id=post_id)
        if post.like.filter(pk=user.id).exists():
            post.like.remove(user)
            return JsonResponse({"remove": "Post unliked successfully.", "like_count": post.like.count()}, status=201)
        else:
            post.like.add(user)
            return JsonResponse({"add": "Post liked successfully.", "like_count": post.like.count()}, status=201)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)