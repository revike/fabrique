# Generated by Django 2.2.10 on 2022-01-11 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_optionanswer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='answer_type',
            new_name='type',
        ),
    ]
