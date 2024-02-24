from .views import *
from django.urls import re_path

urlpatterns = [
    re_path(r'^profile_dashboard$', profile_dashboard, name='profile_dashboard'),
    re_path(r'^profile_personal_info$', profile_personal_info, name='profile_personal_info'),
    re_path(r'^profile_tickets$', profile_tickets, name='profile_tickets'),
    re_path(r'^profile_detail_tickets/(?P<pk>\d+)$', profile_detail_tickets, name='profile_detail_tickets'),

]
