# Generated by Django 4.2.9 on 2024-03-10 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0030_faqcategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Symbol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='Main/Symbol/')),
                ('link', models.TextField(blank=True)),
            ],
        ),
    ]
