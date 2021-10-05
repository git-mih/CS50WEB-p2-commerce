from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listing", views.create_listing, name="create_listing"),
    path("new-entry", views.insert_listing_db, name="insert_listing_db"),
    path("detail/<int:id>", views.details, name="detail"),
    path("place-bid/<int:id>", views.set_bid, name="place_bid"),
    path("close-bid/<int:id>", views.close_bid, name="close_bid"),
    path("wishlist", views.wishlist, name="wishlist"),
    path("addwish/<int:id>", views.add_inside_wishlist, name="add_wish"),
    path("remwish/<int:id>", views.remove_from_wishlist, name="rem_wish"),
    path("categories", views.categories, name="categories"),
    path("filter", views.filter, name="filter"),
    path("comments/<int:id>", views.add_comment, name="add_comment"),
]
