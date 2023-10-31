# Generated by Django 3.2.20 on 2023-10-31 14:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0047_alter_responsefile_file'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='control',
            options={'verbose_name': 'Contrôle', 'verbose_name_plural': 'Contrôles'},
        ),
        migrations.AlterField(
            model_name='control',
            name='reference_code',
            field=models.CharField(error_messages={'unique': 'UNIQUE'}, help_text='Ce code est utilisé notamment pour le dossier de stockage des réponses', max_length=225, unique=True, validators=[django.core.validators.RegexValidator(message='INVALID', regex='^[\\s\\w-]+[^\\.]$')], verbose_name='code de référence'),
        ),
    ]
