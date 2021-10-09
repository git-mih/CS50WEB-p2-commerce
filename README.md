# CS50WEB-p2-commerce

- An eBay-like e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”

## Django version
- 3.2.7

## preview:
- [https://www.youtube.com/watch?v=uTUh2L_D24U](https://www.youtube.com/watch?v=uTUh2L_D24U)
[!["link"](https://i.ytimg.com/vi/uTUh2L_D24U/maxresdefault.jpg)](https://www.youtube.com/watch?v=uTUh2L_D24U)

### How to execute:
1. pip install django
2. py manage.py makemigrations auctions
3. py manage.py migrate
4. py manage.py runserver
5. finally, open the browser and go to http://127.0.0.1:8000/


#### Optionally, before runserver, you can create a super user to access Django default administration panel
1. py manage.py createsuperuser
2. http://127.0.0.1:8000/admin
