# Generated by Django 4.2.9 on 2024-02-25 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0014_cart_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcart',
            name='size',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
