# Generated by Django 4.2.5 on 2023-12-21 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0009_delete_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='type',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
