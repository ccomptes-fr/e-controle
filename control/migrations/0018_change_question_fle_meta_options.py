# Generated by Django 2.1.5 on 2019-01-10 22:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("control", "0017_questionfile_file"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="questionfile",
            options={
                "ordering": ("question", "order"),
                "verbose_name": "Question: Fichier Attaché",
                "verbose_name_plural": "Question: Fichiers Attachés",
            },
        ),
    ]
