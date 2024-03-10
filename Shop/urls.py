from .views import *
from django.urls import re_path

urlpatterns = [
    re_path('^products/$', products, name='products'),
    re_path('^single_product/(?P<title>.+?)$', single_product, name='single_product'),
    re_path('^product_comments/(?P<title>.+?)$',product_comments , name='product_comments'),
    re_path('^cart/$', cart, name='cart'),
    re_path('^cart_number_plus/$', cart_number_plus, name='cart_number_plus'),
    re_path('^cart_number_minus/$', cart_number_minus, name='cart_number_minus'),
    re_path('^shopping/$', shopping, name='shopping'),
    re_path('^shopping_peyment/$', shopping_peyment, name='shopping_peyment'),
    re_path('^shopping_complete_buy/$', shopping_complete_buy, name='shopping_complete_buy'),
    re_path('^my_favorite_product/$', my_favorite_product, name='my_favorite_product'),
    re_path('^add_questions/$', add_questions, name='add_questions'),
    re_path('^products_searchs/$', products_searchs, name='products_searchs'),
    re_path('^search_filter/$', search_filter, name='search_filter'),

]
