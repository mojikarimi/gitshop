# Generated by Django 4.2.5 on 2024-01-02 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0004_customuser_card_number_customuser_national_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='verify_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
