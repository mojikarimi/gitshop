# Generated by Django 4.2.9 on 2024-03-01 18:43

from django.db import migrations, models
import jdatetime


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0008_alter_address_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickets',
            name='date_update',
            field=models.CharField(blank=True, default=jdatetime.datetime.now, max_length=50),
        ),
    ]
