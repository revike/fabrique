# Generated by Django 4.0.1 on 2022-01-15 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0028_remove_answer_option_answer_text_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='option_answer_text',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='main_app.optionanswer', verbose_name='опциональный ответ'),
        ),
    ]