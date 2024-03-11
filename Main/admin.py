from django.contrib import admin
from .models import *
from django.contrib.sessions.models import Session


# Register your models here.
class NoDeleteAdminMixin:
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(MainModel)
class MainModelAdmin(NoDeleteAdminMixin, admin.ModelAdmin):
    def has_add_permission(self, request):
        return not MainModel.objects.exists()


admin.site.register(Menu)
admin.site.register(Footer)
admin.site.register(CatFooter)
admin.site.register(SubCatFooter)
admin.site.register(Visit)
admin.site.register(ChatRoom)
admin.site.register(ChatNew)
admin.site.register(Slider)
admin.site.register(Gif)
admin.site.register(Trend)
admin.site.register(EmailShare)
admin.site.register(Symbol)

admin.site.register(Session)
