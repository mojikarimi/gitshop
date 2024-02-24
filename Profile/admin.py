from django.contrib import admin

# Register your models here.
from Profile.models import Tickets,AnswerTicket

admin.site.register(Tickets)
admin.site.register(AnswerTicket)
