from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import User, Listings, Categories, Bids
from django.urls import reverse

def index(request):
    if request.method == "GET":
        listings = Listings.objects.all()
        print(listings)
        return render(request, "auctions/index.html", {
            "listings": listings
        })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def new_listing(request):
    if request.method == "POST":
        listing_name = request.POST["listing_name"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image_url = request.POST["image_url"]
        category = request.POST["category"]
        category_cleaned = Categories.objects.get(category=category)
        user = request.user
        new_listing = Listings.objects.create(
            name_of_listing=listing_name, listing_description=description, starting_bid=starting_bid,
            image=image_url, listing_category=category_cleaned, listings_owner=user)
        new_listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        categories = Categories.objects.all()
        print(categories)
        return render(request, 'auctions/new_listing.html', {
            "categories": categories
        })


def listing(request, listing_id):
    if request.user.is_authenticated:
        if request.method == "GET":
            listing = Listings.objects.get(pk=listing_id)
            print(listing_id)
            return render(request, 'auctions/listing.html', {
                "listing": listing
            })

def watchlist(request, listing_id, user):
    if request.method == "POST":
        user = request.user
        listing = Listings.objects.get(pk=listing_id)
        user.listings_watchlist.add(listing)
        user.save()
        watchlist = user.listings_watchlist.all()
        return render(request, "auctions/watchlist.html", {
            "listings": watchlist
        })
    else: pass
