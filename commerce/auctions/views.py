from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .models import User, Listings, Categories, Bids, Comments
from django.urls import reverse

def index(request):
    if request.method == "GET":
        listings = Listings.objects.filter(is_closed=False)
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
        last_bidder = Bids.objects.filter(bids_listing=listing_id).order_by('-offer').first()
        all_comments = Comments.objects.filter(listing_commented=listing_id)
        is_in_watchlist = request.user.listings_watchlist.filter(pk=listing_id).exists()
        listing = Listings.objects.get(pk=listing_id)
        my_listing = request.user == listing.listings_owner
        if request.method == "GET":
            return render(request, 'auctions/listing.html', {
                "listing": listing,
                "is_in_watchlist": is_in_watchlist,
                "last_bidder": last_bidder,
                "all_comments": all_comments,
                "my_listing" : my_listing
            })
        else:
            return render(request, 'auctions/listing.html', {
                "listing": listing,
                "is_in_watchlist": is_in_watchlist,
                "last_bidder": last_bidder,
                "all_comments": all_comments,
                "my_listing" : my_listing
            })


def watchlist(request, listing_id):
    user = request.user
    watchlist = user.listings_watchlist.all()
    if request.method == "POST":
        listing = Listings.objects.get(pk=listing_id)
        if request.user.listings_watchlist.filter(pk=listing_id).exists():
            user.listings_watchlist.remove(listing)
            user.save()
        else:
            user.listings_watchlist.add(listing)
            user.save()
        return render(request, "auctions/index.html", {
            "listings": watchlist
        })
    else:
        return render(request, "auctions/index.html", {
            "listings": watchlist
        })

def bid(request, listing_id):
    last_bidder = Bids.objects.filter(bids_listing=listing_id).order_by('-offer').first()
    if request.method == "POST":
        user = request.user
        listing = Listings.objects.get(pk=listing_id)
        offer = int(request.POST["offer"])
        if offer >= listing.starting_bid and (listing.current_bid is None or offer > listing.current_bid):
            new_bid = Bids.objects.create(
                bids_listing=listing, offer=offer, last_bidder=user)
            new_bid.save()
            listing.current_bid = offer
            listing.save()
            HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        else:
            return render(request, "auctions/listing.html", {
                "last_bidder": last_bidder,
                "listing": listing,
                "error": True
            })
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def comment(request, listing_id):
    listing = Listings.objects.get(pk=listing_id)
    if request.method == "POST":
        user = request.user
        comment = request.POST["comment"]
        comment_to_save = Comments(commentator=user, listing_commented=listing, comment=comment)
        comment_to_save.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def close_listing(request, listing_id):
    listing = Listings.objects.get(pk=listing_id)
    user = request.user
    if request.method == "POST":
        if listing.listings_owner == user:
            listing.is_closed = True
            listing.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))