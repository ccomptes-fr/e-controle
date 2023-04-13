# Generated by Django 2.1.7 on 2019-04-01 15:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_profiles", "0005_userprofile_active_directory_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="profile_type",
            field=models.CharField(
                choices=[
                    ("audited", "Organisme Controlé"),
                    ("inspector", "Contrôleur"),
                ],
                max_length=255,
            ),
        ),
    ]
