# Generated by Django 4.2.5 on 2024-01-04 23:55

from django.db import migrations, models
import jdatetime


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0012_visit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='x',
            field=models.CharField(default=jdatetime.datetime.now, max_length=10),
        ),
    ]
