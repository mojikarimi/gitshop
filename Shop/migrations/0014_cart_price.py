# Generated by Django 4.2.9 on 2024-02-25 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0013_productcart_color_productcart_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
