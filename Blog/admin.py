
# Register your models here.
from django.contrib import admin
from .models import *


# Register your models here.
class AdminCategory(admin.ModelAdmin):
    list_display = ['pk', 'title']
    list_display_links = ['pk', 'title']


class AdminSubCategory(admin.ModelAdmin):
    list_display = ['pk', 'title', 'category']
    list_display_links = ['pk', 'title', 'category']


class AdminPost(admin.ModelAdmin):
    list_display = ['pk', 'title', 'category', 'subcategory', 'author']
    list_display_links = ['pk', 'title', 'category', 'subcategory', 'author']


class AdminComments(admin.ModelAdmin):
    list_display = ['pk', 'title', 'status', 'post_id']
    list_display_links = ['pk', 'title', 'post_id']
    list_editable = ['status']


admin.site.register(Category, AdminCategory)
admin.site.register(SubCategory, AdminSubCategory)
admin.site.register(Post, AdminPost)
admin.site.register(Comments, AdminComments)
admin.site.register(OpinionComment)
