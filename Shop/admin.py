from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Group)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(CommentsProduct)
admin.site.register(Cart)
admin.site.register(ProductCart)
admin.site.register(FavoriteProduct)
admin.site.register(Question)
admin.site.register(StarProduct)


