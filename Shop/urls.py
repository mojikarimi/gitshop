from .views import products, search, single_product,product_comments,cart,cart_number_plus,cart_number_minus,shopping
from django.urls import re_path

urlpatterns = [
    re_path('^products/$', products, name='products'),
    re_path('^single_product/(?P<title>.+?)$', single_product, name='single_product'),
    re_path('^search/$', search, name='search'),
    re_path('^product_comments/(?P<title>.+?)$',product_comments , name='product_comments'),
    re_path('^cart/$', cart, name='cart'),
    re_path('^cart_number_plus/$', cart_number_plus, name='cart_number_plus'),
    re_path('^cart_number_minus/$', cart_number_minus, name='cart_number_minus'),
    re_path('^shopping/$', shopping, name='shopping'),

]
