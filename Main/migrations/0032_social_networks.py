# Generated by Django 4.2.9 on 2024-03-10 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0031_symbol'),
    ]

    operations = [
        migrations.CreateModel(
            name='Social_Networks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.CharField(blank=True, max_length=20)),
                ('link', models.TextField(blank=True)),
            ],
        ),
    ]
