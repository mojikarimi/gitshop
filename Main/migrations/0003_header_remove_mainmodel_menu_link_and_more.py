# Generated by Django 4.2.5 on 2023-12-19 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0002_catfooter_footer_subcatfooter'),
    ]

    operations = [
        migrations.CreateModel(
            name='Header',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_name', models.CharField(blank=True, max_length=150)),
                ('menu_link', models.TextField(blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='mainmodel',
            name='menu_link',
        ),
        migrations.RemoveField(
            model_name='mainmodel',
            name='menu_name',
        ),
    ]
