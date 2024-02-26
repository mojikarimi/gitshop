from .views import *
from django.urls import re_path

urlpatterns = [
    re_path(r'^profile_dashboard$', profile_dashboard, name='profile_dashboard'),
    re_path(r'^profile_personal_info$', profile_personal_info, name='profile_personal_info'),
    re_path(r'^profile_tickets$', profile_tickets, name='profile_tickets'),
    re_path(r'^profile_detail_tickets/(?P<pk>\d+)$', profile_detail_tickets, name='profile_detail_tickets'),
    re_path(r'^profile_address/$', profile_address, name='profile_address'),
    re_path(r'^profile_add_address/$', profile_add_address, name='profile_add_address'),
    re_path(r'^profile_edit_address/(?P<pk>\d+)$', profile_edit_address, name='profile_edit_address'),
    re_path(r'^profile_delete_address/(?P<pk>\d+)$', profile_delete_address, name='profile_delete_address'),

]
