from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Categories(models.Model):
    category = models.CharField(max_length=64)
    category_id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.category}"

class Listings(models.Model):
    name_of_listing = models.CharField(max_length=64)
    listing_description = models.TextField(blank=True)
    starting_bid = models.PositiveIntegerField()
    image = models.URLField(max_length=200)
    listings_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_category = models.ForeignKey(Categories, on_delete=models.CASCADE)

class Bids(models.Model):
    bids_listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    bids_current_price = models.PositiveIntegerField(max_length=200)
    last_bidder = models.ForeignKey(User, on_delete=models.CASCADE)

class Comments(models.Model):
    commentator = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_commented = models.ForeignKey(Listings, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    comment_time = models.DateTimeField