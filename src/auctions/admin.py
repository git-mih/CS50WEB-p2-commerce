from django.contrib import admin
from .models import Auction, Bid, Comment, User


admin.site.site_header = "Auction's site Administration"
class AuctionAdmin(admin.ModelAdmin):
    list_display = ("auction", "author", "bid_counter", "created_at")

class BidAdmin(admin.ModelAdmin):
    list_display = ("user", "value", "auction")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "comment", "auction", "created_at")

admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User)