# Generated by Django 4.2.5 on 2023-12-22 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0010_chat_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='user_ip',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
