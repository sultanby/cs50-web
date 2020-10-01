from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    listings_watchlist = models.ManyToManyField('Listings', related_name='Watchlist')

class Categories(models.Model):
    category = models.CharField(max_length=64)
    category_id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.category}"

class Listings(models.Model):
    name_of_listing = models.CharField(max_length=64)
    listing_description = models.TextField(blank=True)
    starting_bid = models.PositiveIntegerField()
    current_bid = models.PositiveIntegerField(null=True)
    image = models.URLField(max_length=200)
    listings_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return f"id of the listing: {self.id}, name: {self.name_of_listing}, "\
               f" starting price: {self.starting_bid}, current bid: {self.current_bid}, owner: {self.listings_owner}," \
               f" category: {self.listing_category}"

class Bids(models.Model):
    bids_listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    offer = models.PositiveIntegerField(null=True)
    last_bidder = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"id is {self.id}, on listing: {self.bids_listing}, current offer is {self.offer}," \
               f"made by: {self.last_bidder}"

class Comments(models.Model):
    commentator = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_commented = models.ForeignKey(Listings, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    comment_time = models.DateTimeField