# Generated by Django 2.1.5 on 2019-01-09 14:59

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("control", "0011_rebuild_theme_order"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="theme",
            name="level",
        ),
        migrations.RemoveField(
            model_name="theme",
            name="lft",
        ),
        migrations.RemoveField(
            model_name="theme",
            name="parent",
        ),
        migrations.RemoveField(
            model_name="theme",
            name="rght",
        ),
        migrations.RemoveField(
            model_name="theme",
            name="tree_id",
        ),
    ]
