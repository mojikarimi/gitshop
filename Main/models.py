from __future__ import unicode_literals
from django.db import models
from jdatetime import datetime


# Create your models here.
class MainModel(models.Model):
    title_website = models.CharField(max_length=150, blank=True)
    title_panel = models.CharField(max_length=150, blank=True)
    icon = models.ImageField(upload_to='Main/icon/%y/%m/%d/', blank=True)
    logo = models.ImageField(upload_to='Main/logo/%y/%m/%d/', blank=True)

    def __str__(self):
        return self.title_website + ' | ' + self.title_panel


class Menu(models.Model):
    menu_name = models.CharField(max_length=150, blank=True)
    menu_link = models.TextField(blank=True)
    number = models.IntegerField(default=0)

    def __str__(self):
        return self.menu_name


class Footer(models.Model):
    text = models.TextField(blank=True)
    copy_right = models.TextField(blank=True)
    image1 = models.ImageField(upload_to='footer/', blank=True)
    link1=models.TextField(blank=True)
    image1_text = models.CharField(max_length=150, blank=True)
    image2 = models.ImageField(upload_to='footer/', blank=True)
    link2=models.TextField(blank=True)
    image2_text = models.CharField(max_length=150, blank=True)
    image3 = models.ImageField(upload_to='footer/', blank=True)
    link3=models.TextField(blank=True)
    image3_text = models.CharField(max_length=150, blank=True)
    image4 = models.ImageField(upload_to='footer/', blank=True)
    link4=models.TextField(blank=True)
    image4_text = models.CharField(max_length=150, blank=True)
    image5 = models.ImageField(upload_to='footer/', blank=True)
    link5=models.TextField(blank=True)
    image5_text = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return 'Footer constants'


class CatFooter(models.Model):
    title = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title


class EmailShare(models.Model):
    email = models.TextField(blank=True)

    def __str__(self):
        return self.email


class SubCatFooter(models.Model):
    cat = models.CharField(max_length=255, blank=True)
    cat_id = models.IntegerField(default=0)
    title = models.TextField(blank=True)
    link = models.TextField(blank=True)

    def __str__(self):
        return self.title + ' | ' + self.cat


class ChatRoom(models.Model):
    user = models.CharField(blank=True, max_length=100)
    ip_client = models.CharField(max_length=50, blank=True)
    date = models.CharField(max_length=150, default=datetime.now)
    admin = models.CharField(blank=True, max_length=150)
    status = models.CharField(max_length=25, blank=True,
                              choices=(('فعال', 'فعال'), ('غیر فعال', 'غیر فعال'), ('اعلام نشده', 'اعلام نشده')))


class ChatNew(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, blank=True)
    text = models.TextField(blank=True)
    type = models.CharField(max_length=25, blank=True, choices=(('client', 'client'), ('admin', 'admin')))
    date = models.CharField(max_length=150, default=datetime.now)
    date_active = models.CharField(max_length=150, blank=True)
    status = models.BooleanField(default=False)


class Visit(models.Model):
    x = models.CharField(max_length=10, default=datetime.now)
    y = models.IntegerField(default=0)


class Gif(models.Model):
    gif = models.FileField(upload_to='Main/gif/%y/%m/%d/', blank=True)
    link = models.TextField(blank=True)

    def __str__(self):
        return 'Gif'


class Slider(models.Model):
    image = models.TextField(blank=True)
    image_url = models.TextField(blank=True)
    link = models.TextField(blank=True)

    def __str__(self):
        return 'images slider'


class Trend(models.Model):
    image = models.TextField(blank=True)
    image_url = models.TextField(blank=True)
    link = models.TextField(blank=True)
    status = models.IntegerField(default=0)

    def __str__(self):
        return 'trend image'
class PictureIndex(models.Model):
    image = models.TextField(blank=True)
    image_url = models.TextField(blank=True)
    link = models.TextField(blank=True)
    size=models.CharField(choices=(('بزرگ', 'بزرگ'), ('کوچک', 'کوچک')),max_length=50,blank=True)
