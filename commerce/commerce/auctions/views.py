from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, auction_listings, bids, comments, watchlist


def index(request):
    listings = auction_listings.objects.filter(active=True)
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
    
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image_url = request.POST.get("image_url")
        category = request.POST.get("category")
        
        if not title or not description or not starting_bid:
            return render(request, "auctions/create_listing.html", {
                "message": "Title, description, and starting bid are required."
            })
        
        listing = auction_listings(
            title = title,
            description = description,
            starting_bid = starting_bid,
            image_url = image_url,
            category = category
        )
        listing.save()
        return HttpResponseRedirect(reverse("index"))
        
    return render(request, "auctions/create_listing.html")

def listing_detail(request, id):
    # refactorizar request method post
    listing_item = auction_listings.objects.get(id=id)
    user_watchlist = None
    if request.user.is_authenticated:
        user_watchlist = watchlist.objects.filter(user=request.user, listing=listing_item)

    if request.method == "POST":
            if user_watchlist.exists():
                user_watchlist.delete()
            else:
                new_item = watchlist(user=request.user, listing=listing_item)
                new_item.save()
            return HttpResponseRedirect(reverse("listing_detail", args=(id,)))

    return render (request, "auctions/listing_detail.html", {
        "listing": listing_item,
        "user_watchlist": user_watchlist
    })
