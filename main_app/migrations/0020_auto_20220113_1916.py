# Generated by Django 2.2.10 on 2022-01-13 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0019_auto_20220113_1752'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='option_answer_text',
        ),
        migrations.AddField(
            model_name='answer',
            name='option_answer_text',
            field=models.ManyToManyField(related_name='answer', to='main_app.OptionAnswer', verbose_name='опциональный ответ'),
        ),
    ]