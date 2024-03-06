from __future__ import unicode_literals
from django.db import models
from jdatetime import datetime


class Group(models.Model):
    class Meta:
        verbose_name_plural = 'product groups'

    name = models.CharField(max_length=150, blank=True)
    image = models.ImageField(blank=True, upload_to='Group/ImageGroup/%y/%m/%d/')

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'product categories'

    name = models.CharField(max_length=150, blank=True)
    group = models.CharField(max_length=150, blank=True)
    group_id = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    class Meta:
        verbose_name_plural = 'product subcategories'

    name = models.CharField(max_length=150, blank=True)
    group = models.CharField(max_length=150, blank=True)
    group_id = models.IntegerField(default=0)
    category = models.CharField(max_length=150, blank=True)
    category_id = models.IntegerField(default=0)

    def __str__(self):
        return self.name


# Create your models here.
class Product(models.Model):
    class Meta:
        verbose_name_plural = 'Product'

    name_product = models.TextField(blank=True)
    name_product_english = models.TextField(blank=True)
    group = models.CharField(max_length=150, blank=True)
    group_id = models.IntegerField(default=0)
    category = models.CharField(max_length=150, blank=True)
    category_id = models.IntegerField(default=0)
    sub_category = models.CharField(max_length=150, blank=True)
    sub_category_id = models.IntegerField(default=0)
    color = models.TextField(blank=True)
    size = models.TextField(blank=True)
    description = models.TextField(blank=True)
    image1 = models.ImageField(upload_to='PanelProduct/ImageProduct/%y/%m/%d/', blank=True)
    image2 = models.ImageField(upload_to='PanelProduct/ImageProduct/%y/%m/%d/', blank=True)
    image3 = models.ImageField(upload_to='PanelProduct/ImageProduct/%y/%m/%d/', blank=True)
    image4 = models.ImageField(upload_to='PanelProduct/ImageProduct/%y/%m/%d/', blank=True)
    video = models.FileField(upload_to='PanelProduct/VideoProduct/%y/%m/%d/', blank=True)
    attribute_title = models.TextField(blank=True)
    attribute_value = models.TextField(blank=True)
    title_text = models.TextField(blank=True)
    full_text = models.TextField(blank=True)
    price = models.IntegerField(default=0)
    discount_percent = models.IntegerField(default=0)
    discount_period = models.CharField(max_length=10)
    discounted_price = models.IntegerField(default=0)
    instant_sale = models.BooleanField(default=False)
    amazing_offer = models.BooleanField(default=False)
    our_suggestion = models.BooleanField(default=False)
    available = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    sales_number = models.IntegerField(default=0)
    number = models.IntegerField(default=0)
    date = models.CharField(max_length=10, blank=True)
    view = models.IntegerField(default=0)
    order_number = models.IntegerField(default=0)

    def __str__(self):
        return self.name_product


class CommentsProduct(models.Model):
    pk_product = models.IntegerField(default=0)
    user = models.TextField(blank=True)
    user_id = models.IntegerField(default=0)
    build = models.IntegerField(default=0)
    innovation = models.IntegerField(default=0)
    ease_of_use = models.IntegerField(default=0)
    designing = models.IntegerField(default=0)
    possibilities = models.IntegerField(default=0)
    worth_buying = models.IntegerField(default=0)
    title = models.TextField(blank=True)
    strengths = models.TextField(blank=True)
    weaknesses = models.TextField(blank=True)
    text = models.TextField(blank=True)
    tender = models.CharField(max_length=75, blank=True)
    confirmed = models.BooleanField(default=False)
    date = models.CharField(max_length=50, default=datetime.now)

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.CharField(max_length=150, blank=True)
    user_id = models.IntegerField(default=0)
    address_id = models.IntegerField(default=0)
    sending_method = models.IntegerField(default=0)
    bill = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    price = models.IntegerField(default=0)
    order_code = models.CharField(max_length=50, blank=True)
    date = models.CharField(default=datetime.now, max_length=10)
    cancel = models.BooleanField(default=False)
    preparation = models.BooleanField(default=False)
    exit = models.BooleanField(default=False)
    delivery = models.BooleanField(default=False)
    exchange = models.BooleanField(default=False)
    customer = models.BooleanField(default=False)


class ProductCart(models.Model):
    cart_id = models.IntegerField(default=0)
    product_id = models.IntegerField(default=0)
    size = models.CharField(max_length=25, blank=True, null=True)
    color = models.CharField(max_length=25, blank=True)
    number = models.IntegerField(default=1)


class FavoriteProduct(models.Model):
    user = models.CharField(max_length=150, blank=True)
    user_id = models.IntegerField(default=0)
    product_id = models.IntegerField(default=0)
    status = models.CharField(blank=True, max_length=1)


class Question(models.Model):
    product_id = models.IntegerField(default=0)
    user = models.CharField(max_length=150, blank=True)
    user_id = models.IntegerField(default=0)
    text = models.TextField(blank=True)
    date = models.CharField(max_length=50, default=datetime.now)
    status = models.BooleanField(default=False)
    answer_text = models.TextField(blank=True,default='')
    answer_date = models.CharField(max_length=50, default='')
    faq = models.BooleanField(default=False)
    sort = models.IntegerField(default=0)
