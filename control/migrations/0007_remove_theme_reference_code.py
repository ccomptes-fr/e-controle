# Generated by Django 2.1.4 on 2018-12-20 10:44

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("control", "0006_change_meta_options"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="theme",
            name="reference_code",
        ),
    ]
