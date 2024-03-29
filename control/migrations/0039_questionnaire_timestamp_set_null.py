# Generated by Django 2.2.8 on 2019-12-24 10:31

from django.db import migrations


def set_timestamp_null(apps, schema_editor):
    Questionnaire = apps.get_model("control", "Questionnaire")
    Questionnaire.objects.update(modified=None)


class Migration(migrations.Migration):
    dependencies = [
        ("control", "0038_add_timestamp_on_questionnaire"),
    ]

    operations = [
        migrations.RunPython(
            set_timestamp_null, reverse_code=lambda apps, schema_editor: None
        )
    ]
