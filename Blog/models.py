from __future__ import unicode_literals
# Create your models here.
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Category(models.Model):
    # blog category
    class Meta:
        verbose_name_plural = 'blog categores'

    title = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    # blog sub category
    class Meta:
        verbose_name_plural = 'blog sub categores'

    title = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=255, blank=True)
    category_id = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.title + f' ({self.category})'


class Post(models.Model):
    # model for create a post for blog
    class Meta:
        verbose_name_plural = 'Post details'

    title = models.TextField(blank=True)
    full_text = models.TextField(blank=True)
    category = models.CharField(max_length=255, blank=True)
    category_id = models.IntegerField(blank=True, default=0)
    subcategory = models.CharField(max_length=255, blank=True)
    subcategory_id = models.IntegerField(blank=True, default=0)
    image = models.TextField(blank=True)
    image_url = models.TextField(blank=True)
    author = models.CharField(blank=True, max_length=100)
    date = models.CharField(max_length=10, blank=True)
    view = models.IntegerField(default=0, blank=True)
    tags = models.TextField(blank=True)
    score = models.IntegerField(default=0)
    usrer_id = models.IntegerField(default=0)

    def __str__(self):
        return self.title + f' ({self.view})'


class Comments(models.Model):
    # post comments
    class Meta:
        verbose_name_plural = 'Comments For Posts '

    title = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    post_id = models.IntegerField(default=0, blank=True)
    date = models.CharField(max_length=10, blank=True)
    status = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    user = models.TextField(blank=True)
    user_id = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    dis_like = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class OpinionComment(models.Model):
    # like and dislike for comment
    opinion = models.IntegerField(default=0, blank=True)
    comment_id = models.IntegerField(default=0, blank=True)
    user_id = models.IntegerField(default=0, blank=True)
    user = models.TextField(blank=True)

    def __str__(self):
        if self.opinion == 1:
            return 'Like'
        elif self.opinion == -1:
            return 'Dis Like'
        else:
            return 'No Opinion'
