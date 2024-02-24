from .views import *
from django.urls import re_path

urlpatterns = [
    re_path(r'^$', index, name='index'),
    re_path(r'^update_chat$', update_chat, name='update_chat'),
    re_path(r'^new_chat$', new_chat, name='new_chat'),
]
