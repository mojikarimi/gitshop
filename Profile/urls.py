from .views import *
from django.urls import re_path

urlpatterns = [
    re_path(r'^profile_dashboard$', profile_dashboard, name='profile_dashboard'),
    re_path(r'^profile_personal_info$', profile_personal_info, name='profile_personal_info'),
    re_path(r'^profile_tickets$', profile_tickets, name='profile_tickets'),
    re_path(r'^profile_tickets_detail/(?P<pk>\d+)$', profile_tickets_detail, name='profile_tickets_detail'),
    re_path(r'^profile_address/$', profile_address, name='profile_address'),
    re_path(r'^profile_add_address/$', profile_add_address, name='profile_add_address'),
    re_path(r'^profile_edit_address/(?P<pk>\d+)$', profile_edit_address, name='profile_edit_address'),
    re_path(r'^profile_delete_address/(?P<pk>\d+)$', profile_delete_address, name='profile_delete_address'),
    re_path(r'^profile_user_history/$', profile_user_history, name='profile_user_history'),
    re_path(r'^profile_orders/$', profile_orders, name='profile_orders'),
    re_path(r'^profile_details_order/(?P<order_code>.+?)$', profile_details_order, name='profile_details_order'),
    re_path(r'^profile_my_favorite/$', profile_my_favorite, name='profile_my_favorite'),
    re_path(r'^profile_comments/$', profile_comments, name='profile_comments'),
    re_path(r'^profile_delete_my_favorite/(?P<pk>\d+)$', profile_delete_my_favorite, name='profile_delete_my_favorite'),
    re_path(r'^profile_change_password/$', profile_change_password, name='profile_change_password'),

]
