from .views import *
from django.urls import re_path
from Blog import views as blogview
from Account import views as Accountview
from Shop import views as shopview
from Main import views as mainview

urlpatterns = [
    # APP Panel Panel URLs
    re_path(r'^(?P<month>\d*)$', panel_index, name='panel_index'),
    # APP Blog Panel URLs
    re_path(r'^panel_creat_post_blog$', blogview.panel_add_post, name='panel_add_post'),
    re_path(r'^panel_add_category$', blogview.panel_add_category, name='panel_add_category'),
    re_path(r'^panel_delete_category/(?P<pk>\d+)$', blogview.panel_delete_category, name='panel_delete_category'),
    re_path(r'^panel_edit_category/(?P<pk>\d+)$', blogview.panel_edit_category, name='panel_edit_category'),
    re_path(r'^panel_add_sub_category$', blogview.panel_add_sub_category, name='panel_add_sub_category'),
    re_path(r'^panel_delete_sub_category/(?P<pk>\d+)$', blogview.panel_delete_sub_category,
            name='panel_delete_sub_category'),
    re_path(r'^panel_edit_sub_category/(?P<pk>\d+)$', blogview.panel_edit_sub_category, name='panel_edit_sub_category'),
    re_path(r'^panel_add_post$', blogview.panel_add_post, name='panel_add_post'),
    re_path(r'^panel_post_lists$', blogview.panel_post_lists, name='panel_post_lists'),
    re_path(r'^panel_delete_post/(?P<pk>\d+)$', blogview.panel_delete_post, name='panel_delete_post'),
    re_path(r'^panel_edit_post/(?P<pk>\d+)$', blogview.panel_edit_post, name='panel_edit_post'),
    re_path(r'^panel_comments/(?P<pk>\d+)$', blogview.panel_comments, name='panel_comments'),
    re_path(r'^panel_comments_edit/(?P<pk>\d+)$', blogview.panel_comments_edit, name='panel_comments_edit'),
    re_path(r'^panel_comments_delete/(?P<pk>\d+)$', blogview.panel_comments_delete, name='panel_comments_delete'),

    # APP User Panel URLs
    re_path(r'^panel_list_user$', Accountview.panel_list_user, name='panel_list_user'),
    re_path(r'^panel_add_group_user$', Accountview.panel_add_group_user, name='panel_add_group_user'),
    re_path(r'^panel_delete_group_user/(?P<pk>\d+)$', Accountview.panel_delete_group_user,
            name='panel_delete_group_user'),
    re_path(r'^panel_details_group/(?P<pk>\d+)$', Accountview.panel_details_group, name='panel_details_group'),

    re_path(r'^panel_permissions/(?P<pk>\d+)$', Accountview.panel_permissions, name='panel_permissions'),
    re_path(r'^panel_user_access/(?P<pk>\d+)$', Accountview.panel_user_access, name='panel_user_access'),
    re_path(r'^panel_delete_user/(?P<pk>\d+)$', Accountview.panel_delete_user, name='panel_delete_user'),
    # APP Shop Panel URLs
    re_path(r'^panel_add_product$', shopview.panel_add_product, name='panel_add_product'),
    re_path(r'^panel_list_product$', shopview.panel_list_product, name='panel_list_product'),
    re_path(r'^panel_edit_product/(?P<pk>\d+)$', shopview.panel_edit_product, name='panel_edit_product'),
    re_path(r'^panel_delete_product/(?P<pk>\d+)$', shopview.panel_delete_product, name='panel_delete_product'),
    re_path(r'^panel_add_group_product$', shopview.panel_add_group_product, name='panel_add_group_product'),
    re_path(r'^panel_add_category_product$', shopview.panel_add_category_product, name='panel_add_category_product'),
    re_path(r'^panel_add_subcategory_product$', shopview.panel_add_subcategory_product,
            name='panel_add_subcategory_product'),
    re_path(r'^panel_delete_group_product/(?P<pk>\d+)$', shopview.panel_delete_group_product,
            name='panel_delete_group_product'),
    re_path(r'^panel_delete_category_product/(?P<pk>\d+)$', shopview.panel_delete_category_product,
            name='panel_delete_category_product'),
    re_path(r'^panel_delete_subcategory_product/(?P<pk>\d+)$', shopview.panel_delete_subcategory_product,
            name='panel_delete_subcategory_product'),
    re_path(r'^panel_edit_group_product/(?P<pk>\d+)$', shopview.panel_edit_group_product,
            name='panel_edit_group_product'),
    re_path(r'^panel_edit_category_product/(?P<pk>\d+)$', shopview.panel_edit_category_product,
            name='panel_edit_category_product'),
    re_path(r'^panel_edit_subcategory_product/(?P<pk>\d+)$', shopview.panel_edit_subcategory_product,
            name='panel_edit_subcategory_product'),
    re_path(r'^panel_view_cart$', shopview.panel_view_cart,
            name='panel_view_cart'),
    re_path(r'^panel_details_cart/(?P<pk>\d+)$', shopview.panel_details_cart,
            name='panel_details_cart'),
    re_path(r'^panel_comments_product/(?P<pk_product>\d+)$', shopview.panel_comments_product,
            name='panel_comments_product'),
    re_path(r'^panel_details_comments/(?P<pk_comment>\d+)$', shopview.panel_details_comments,
            name='panel_details_comments'),
    re_path(r'^panel_delete_comment/(?P<pk_comment>\d+)$', shopview.panel_delete_comment,
            name='panel_delete_comment'),
    re_path(r'^panel_questions_list/(?P<pk>\d+)$', shopview.panel_questions_list, name='panel_questions_list'),
    re_path(r'^panel_sort_question/(?P<pk>\d+)$', shopview.panel_sort_question, name='panel_sort_question'),
    re_path(r'^panel_details_question/(?P<pk>\d+)$', shopview.panel_details_question,
            name='panel_details_question'),
re_path(r'^panel_delete_question/(?P<pk>\d+)$', shopview.panel_delete_question,
            name='panel_delete_question'),

    # APP Main Panel URLs
    re_path(r'^panel_tickets_lists$', mainview.panel_tickets_lists, name='panel_tickets_lists'),
    re_path(r'^panel_answer_tickets/(?P<pk>\d+)$', mainview.panel_answer_tickets, name='panel_answer_tickets'),
    re_path(r'^panel_change_status_ticket/(?P<pk>\d+)$', mainview.panel_change_status_ticket,
            name='panel_change_status_ticket'),
    re_path(r'^panel_add_cat_footer$', mainview.panel_add_cat_footer, name='panel_add_cat_footer'),
    re_path(r'^panel_edit_cat_footer/(?P<pk>\d+)$', mainview.panel_edit_cat_footer, name='panel_edit_cat_footer'),
    re_path(r'^panel_delete_cat_footer/(?P<pk>\d+)$', mainview.panel_delete_cat_footer, name='panel_delete_cat_footer'),

    re_path(r'^panel_add_subcat_footer/(?P<pk>\d+)$', mainview.panel_add_subcat_footer, name='panel_add_subcat_footer'),
    re_path(r'^panel_delete_subcat_footer/(?P<pk>\d+)$', mainview.panel_delete_subcat_footer,
            name='panel_delete_subcat_footer'),
    re_path(r'^panel_edit_subcat_footer/(?P<pk>\d+)$', mainview.panel_edit_subcat_footer,
            name='panel_edit_subcat_footer'),

    re_path(r'^panel_add_menu$', mainview.panel_add_menu, name='panel_add_menu'),
    re_path(r'^panel_edit_menu/(?P<pk>\d+)$', mainview.panel_edit_menu, name='panel_edit_menu'),
    re_path(r'^panel_delete_menu/(?P<pk>\d+)$', mainview.panel_delete_menu, name='panel_delete_menu'),
    re_path(r'^panel_sort_menu/$', mainview.panel_sort_menu, name='panel_sort_menu'),

    re_path(r'^panel_footer$', mainview.panel_footer, name='panel_footer'),
    re_path(r'^panel_main_model$', mainview.panel_main_model, name='panel_main_model'),

    re_path(r'^panel_gif$', mainview.panel_gif, name='panel_gif'),
    re_path(r'^panel_add_slider$', mainview.panel_add_slider, name='panel_add_slider'),
    re_path(r'^panel_edit_slider/(?P<pk>\d+)$', mainview.panel_edit_slider, name='panel_edit_slider'),
    re_path(r'^panel_delete_slider/(?P<pk>\d+)$', mainview.panel_delete_slider, name='panel_delete_slider'),
    re_path(r'^panel_trend$', mainview.panel_trend, name='panel_trend'),

    # chat views
    re_path(r'^panel_new_chat$', mainview.panel_new_chat, name='panel_new_chat'),
    re_path(r'^panel_update_chat$', mainview.panel_update_chat, name='panel_update_chat'),
    re_path(r'^panel_chat$', mainview.panel_chat, name='panel_chat'),
    re_path(r'^panel_massages/(?P<pk>\d+)$', mainview.panel_massages, name='panel_massages'),
    re_path(r'^panel_change_status$', mainview.panel_change_status, name='panel_change_status'),
]
