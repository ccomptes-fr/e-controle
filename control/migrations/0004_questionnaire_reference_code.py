# Generated by Django 2.1.4 on 2018-12-12 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0003_control_reference_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaire',
            name='reference_code',
            field=models.CharField(blank=True, help_text='Ce code est utilisé notamment pour le dossier de stockage des réponses', max_length=255, verbose_name='code de référence'),
        ),
    ]