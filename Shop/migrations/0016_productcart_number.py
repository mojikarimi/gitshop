# Generated by Django 4.2.9 on 2024-02-25 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0015_alter_productcart_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcart',
            name='number',
            field=models.IntegerField(default=1),
        ),
    ]
