# Generated by Django 4.2.9 on 2024-03-04 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0009_alter_tickets_date_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickets',
            name='user_ip',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
