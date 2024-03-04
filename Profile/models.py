from __future__ import unicode_literals
from django.db import models
from jdatetime import datetime


# Create your models here.
class Tickets(models.Model):
    ticket_id = models.IntegerField(default=0)
    subject = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True)
    manager = models.CharField(max_length=150, blank=True)
    manager_id = models.IntegerField(default=0)
    date = models.CharField(default=datetime.now, max_length=50)
    date_update = models.CharField(max_length=50, blank=True, default=datetime.now)
    user = models.CharField(max_length=255, blank=True)
    user_id = models.IntegerField(default=0)
    status = models.CharField(max_length=150, blank=True)
    user_ip=models.CharField(blank=True,max_length=150)

    def __str__(self):
        return self.subject


class AnswerTicket(models.Model):
    ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE)
    user = models.CharField(max_length=255, blank=True)
    user_id = models.IntegerField(default=0)
    type_user = models.CharField(max_length=40, blank=True)
    text = models.TextField(blank=True)
    date = models.CharField(default=datetime.now, max_length=10)


class Address(models.Model):
    user = models.CharField(max_length=150, blank=True)
    user_id = models.IntegerField(default=0)
    city = models.CharField(max_length=150, blank=True)
    state = models.CharField(max_length=150, blank=True)
    postal_code = models.CharField(max_length=25, blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=250, blank=True)
    status = models.IntegerField(default=1)
