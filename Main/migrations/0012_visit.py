# Generated by Django 4.2.5 on 2024-01-04 23:44

from django.db import migrations, models
import jdatetime


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0011_chat_user_ip'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.DateField(default=jdatetime.datetime.now)),
                ('y', models.IntegerField(default=0)),
            ],
        ),
    ]
