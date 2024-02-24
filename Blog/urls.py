from .views import *
from django.urls import re_path

urlpatterns = [
    re_path(r'^$', blog, name='blog'),
    re_path(r'^post/comment/(?P<pk>\d+)$', comment_post, name='comment_post'),
    re_path(r'^post/(?P<title>.+?)$', post, name='post'),
    re_path(r'^like_system/$', like_system, name='like_system'),

]
