# Generated by Django 2.2.10 on 2022-01-11 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_auto_20220111_0923'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='type',
            new_name='answer_type',
        ),
    ]
