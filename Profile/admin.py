from django.contrib import admin

# Register your models here.
from Profile.models import Tickets,AnswerTicket,Address

admin.site.register(Tickets)
admin.site.register(AnswerTicket)
admin.site.register(Address)
