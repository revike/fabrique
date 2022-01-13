# Generated by Django 4.0.1 on 2022-01-13 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0021_remove_answer_option_answer_text_and_more'),
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
