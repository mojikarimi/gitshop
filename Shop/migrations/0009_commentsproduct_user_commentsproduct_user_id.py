# Generated by Django 4.2.5 on 2023-12-18 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0008_rename_buying_commentsproduct_worth_buying_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentsproduct',
            name='user',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='commentsproduct',
            name='user_id',
            field=models.IntegerField(default=0),
        ),
    ]
