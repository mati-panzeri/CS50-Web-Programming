from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class auction_listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    starting_bid = models.FloatField()
    current_bid = models.FloatField(blank=True, null=True)
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=64, blank=True)

class bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(auction_listings, on_delete=models.CASCADE, related_name="bids")
    bid_amount = models.FloatField()

class comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(auction_listings, on_delete=models.CASCADE, related_name="comments")

