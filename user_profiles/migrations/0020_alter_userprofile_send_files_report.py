# Generated by Django 3.2.13 on 2022-07-04 09:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_profiles", "0019_auto_20210802_1553"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="send_files_report",
            field=models.BooleanField(
                default=True,
                help_text="Envoyer par email le rapport des fichiers déposés ?",
                verbose_name="Envoi Rapport de Fichiers",
            ),
        ),
    ]
