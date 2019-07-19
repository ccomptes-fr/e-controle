# Generated by Django 2.1.9 on 2019-07-15 13:31

import control.upload_path
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0028_rename_to_uploaded_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionnaire',
            name='generated_file',
            field=models.FileField(blank=True, help_text='Ce fichier est généré automatiquement quand le questionnaire est enregistré.', null=True, upload_to=control.upload_path.questionnaire_file_path, verbose_name='fichier du questionnaire généré automatiquement'),
        ),
        migrations.AlterField(
            model_name='questionnaire',
            name='uploaded_file',
            field=models.FileField(blank=True, help_text='Si ce fichier est renseigné, il sera proposé au téléchargement.Sinon, un fichier généré automatiquement sera disponible.', null=True, upload_to=control.upload_path.questionnaire_file_path, verbose_name='fichier du questionnaire'),
        ),
    ]
