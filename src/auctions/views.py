from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from .models import User, Auction, Bid, Comment
from .forms import CreateCommentForm, CreateListingForm


def index(request):
    queryset = Auction.objects.all()
    return render(request, "auctions/index.html", {
        'objects': queryset,
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


@login_required(login_url='auctions/login.html')
def create_listing(request):
    form = CreateListingForm()
    return render(request, "auctions/create_listing.html", {
        'form': form
    })


@login_required(login_url='auctions/login.html')
def insert_listing_db(request):
    form = CreateListingForm(request.POST)
    if form.is_valid():
        auction = Auction(author=request.user, **form.cleaned_data)
        auction.save()
        initial_bid = auction.initial_bid
        initial_bid = Bid(value=initial_bid, user=request.user, auction=auction)
        initial_bid.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'auctions/create_listing.html', {
            'form': form,
            'error': form.errors
        })


def details(request, id):
    query = Auction.objects.get(pk=id)
    bid = get_object_or_404(Bid, auction=query)
    comments = Comment.objects.filter(auction=query)
    return render(request, 'auctions/detail.html', {
        'auction': query,
        'user': request.user,
        'bid': bid,
        'comments': comments,
        'comment_form': CreateCommentForm()
    })

@login_required(login_url='auctions/login.html')
def set_bid(request, id):
    value = request.POST['bid']
    if value:
        value = float(value)
        auction = get_object_or_404(Auction, id=id)
        if value > get_object_or_404(Bid, id=id).value:
            bid = get_object_or_404(Bid, id=id)
            bid.value = value
            bid.user = request.user
            bid.save()
            auction.bid_counter += 1
            auction.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            raise ValidationError('Bid must be greater than current Bid value')
    else:
        raise ValidationError('Bid must be greater than Current Bid value')


@login_required(login_url='auctions/login.html')
def close_bid(request, id):
    auction = get_object_or_404(Auction, id=id)
    auction.status = False
    auction.save()
    return HttpResponseRedirect(reverse('index'))


@login_required(login_url='auctions/login.html')
def wishlist(request):
    queryset = request.user.wishlist
    print(queryset)
    return render(request, 'auctions/wishlist.html', {
        'queryset': queryset.all()
    })

def add_inside_wishlist(request, id):
    auction = get_object_or_404(Auction, id=id)
    request.user.wishlist.add(auction)
    request.user.wishlist_counter += 1
    request.user.save()
    return HttpResponseRedirect(reverse('index'))

def remove_from_wishlist(request, id):
    auction = get_object_or_404(Auction, id=id)
    request.user.wishlist.remove(auction)
    request.user.wishlist_counter -= 1
    request.user.save()
    if '/remwish/' in request.path:
        return HttpResponseRedirect(reverse('index'))
    return HttpResponseRedirect(reverse('wishlist'))

def categories(request):
    return render(request, 'auctions/categories.html')

def filter(request):
    q = request.GET['category'].lower()
    queryset = Auction.objects.filter(category=q)
    return render(request, 'auctions/category.html', {
        'queryset': queryset
    })
    
def add_comment(request, id):
    anonymous = User.first_name
    if request.user is not anonymous:
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            f = form.cleaned_data
            com = Comment(
                user=request.user, 
                auction=get_object_or_404(Auction, id=id),
                **f
            )
            com.save()
            return HttpResponseRedirect(reverse('detail', kwargs={
                'id': id
            }))
    else:
        return render(request, 'auctions/login.html', {
            'message': 'Must be logged in to be able to comment'
        })
