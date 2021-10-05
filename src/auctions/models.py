from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    wishlist_counter = models.IntegerField(default=0, blank=True)
    wishlist = models.ManyToManyField('Auction')
    pass

class Auction(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.CharField(max_length=64)
    note = models.CharField(max_length=254)
    est_retail = models.FloatField(blank=True)
    initial_bid = models.FloatField()
    bid_counter = models.IntegerField(default=1)
    status = models.BooleanField(default=True)
    category = models.CharField(max_length=64, blank=True)
    thumbnail = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.auction} ({self.author})'


class Bid(models.Model):
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bid')

    def __str__(self):
        return f'{self.value} from {self.user}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=254)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'({self.user} {self.auction}) comment: {self.comment}'