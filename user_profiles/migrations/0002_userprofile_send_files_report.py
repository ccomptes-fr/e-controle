# Generated by Django 2.1.5 on 2019-02-18 10:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_profiles", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="send_files_report",
            field=models.BooleanField(
                default=False,
                help_text="Envoyer par email le rapport des fichiers uplodés ?",
                verbose_name="Envoie Rapport de Fichiers",
            ),
        ),
    ]
