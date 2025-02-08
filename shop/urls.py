from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.register, name="register"),
    path('login', views.login_page, name="login"),
    path('logout', views.logout_page, name="logout"),
    path('cart', views.cart_page, name="cart"),
    path('remove_cart/<str:cid>', views.remove_cart, name="remove_cart"),
    path('collections', views.collections, name="collections"),
    path('collections/<str:name>', views.collectionsview, name="collections"),
    path('collections/<str:cname>/<str:pname>', views.product_details, name="product_details"),
    path('addtocart', views.add_to_cart, name="addtocart"),
    path('placeorder', views.place_order, name="placeorder"),
    path('order-summary', views.order_summary, name="order_summary"),
    path('remove_order/<int:oid>', views.remove_order, name="remove_order"),  # URL pattern for removing order
    path('buynow', views.buy_now, name="buynow"),
]



 