from .views import *
from django.urls import re_path


urlpatterns = [
    re_path(r'^signup$', signup, name='signup'),
    re_path(r'^signin$', signin, name='signin'),
    re_path(r'^signout$', signout, name='signout'),
    re_path(r'^verify_email$', verify_email, name='verify_email'),
]
