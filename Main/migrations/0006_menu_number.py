# Generated by Django 4.2.5 on 2023-12-19 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0005_rename_header_menu'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='number',
            field=models.IntegerField(default=0),
        ),
    ]
