# Generated by Django 4.0.1 on 2022-01-16 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0034_remove_answer_option_answer_text_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='option_answer_text_id',
        ),
        migrations.AddField(
            model_name='answer',
            name='option_answer_text_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='main_app.optionanswer', verbose_name='опциональный ответ'),
        ),
    ]