# Generated by Django 4.2.9 on 2024-03-06 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0027_alter_question_answer_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answer_text',
            field=models.TextField(default=''),
        ),
    ]
