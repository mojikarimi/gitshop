# Generated by Django 4.2.9 on 2024-02-27 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0017_product_order_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='order_code',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
