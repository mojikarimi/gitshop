# Generated by Django 4.2.5 on 2023-12-18 22:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0007_commentsproduct_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commentsproduct',
            old_name='buying',
            new_name='worth_buying',
        ),
        migrations.RemoveField(
            model_name='commentsproduct',
            name='worth',
        ),
    ]
