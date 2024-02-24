from .views import products, search, single_product,product_comments
from django.urls import re_path

urlpatterns = [
    re_path('^products/$', products, name='products'),
    re_path('^single_product/(?P<title>.+?)$', single_product, name='single_product'),
    re_path('^search/$', search, name='search'),
    re_path('^product_comments/(?P<title>.+?)$',product_comments , name='product_comments'),

]
