from .views import *
from django.urls import re_path

urlpatterns = [
    re_path(r'^$', index, name='index'),
    re_path(r'^update_chat$', update_chat, name='update_chat'),
    re_path(r'^new_chat$', new_chat, name='new_chat'),
    re_path(r'^faq$', faq, name='faq'),
    re_path(r'^faq_details/(?P<category>.+?)$', faq_details, name='faq_details'),
    re_path(r'^email_shair$', email_shair, name='email_shair'),
]
