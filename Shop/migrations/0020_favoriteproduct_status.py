# Generated by Django 4.2.9 on 2024-02-28 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0019_favoriteproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='favoriteproduct',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
