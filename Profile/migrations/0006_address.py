# Generated by Django 4.2.9 on 2024-02-26 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0005_remove_tickets_date_closed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=150)),
                ('user_id', models.IntegerField(default=0)),
                ('city', models.CharField(blank=True, max_length=150)),
                ('state', models.CharField(blank=True, max_length=150)),
                ('postal_code', models.CharField(blank=True, max_length=25)),
                ('address', models.TextField(blank=True)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('name', models.CharField(blank=True, max_length=250)),
            ],
        ),
    ]
