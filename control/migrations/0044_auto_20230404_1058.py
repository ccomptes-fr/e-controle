# Generated by Django 3.2.13 on 2023-04-04 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0043_questionnaire_is_finalized'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaire',
            name='is_closed',
            field=models.BooleanField(default=False, help_text='Ce questionnaire a-t-il été accepté par le contrôleur ?', verbose_name='terminé'),
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='is_not_closed',
            field=models.BooleanField(default=False, help_text='Ce questionnaire a-t-il été non accepté par le contrôleur ?', verbose_name='non terminé'),
        ),
    ]