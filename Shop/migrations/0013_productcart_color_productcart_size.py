# Generated by Django 4.2.9 on 2024-02-25 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0012_cart_productcart'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcart',
            name='color',
            field=models.CharField(blank=True, max_length=25),
        ),
        migrations.AddField(
            model_name='productcart',
            name='size',
            field=models.CharField(blank=True, max_length=25),
        ),
    ]
