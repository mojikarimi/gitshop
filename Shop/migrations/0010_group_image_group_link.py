# Generated by Django 4.2.9 on 2024-02-08 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0009_commentsproduct_user_commentsproduct_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='image',
            field=models.ImageField(blank=True, upload_to='Group/ImageGroup/%y/%m/%d/'),
        ),
        migrations.AddField(
            model_name='group',
            name='link',
            field=models.TextField(blank=True),
        ),
    ]
