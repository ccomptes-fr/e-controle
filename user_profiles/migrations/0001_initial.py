# Generated by Django 2.1.4 on 2018-12-12 23:49

import annoying.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("control", "0006_change_meta_options"),
        ("auth", "0009_alter_user_last_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "user",
                    annoying.fields.AutoOneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="profile",
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "profile_type",
                    models.CharField(
                        choices=[
                            ("audited", "Organisme Controlé"),
                            ("inspector", "Controleur"),
                        ],
                        max_length=255,
                    ),
                ),
                (
                    "organization",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Organisme"
                    ),
                ),
                (
                    "control",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="user_profiles",
                        to="control.Control",
                        verbose_name="controle",
                    ),
                ),
            ],
            options={
                "verbose_name": "Profile Utilisateur",
                "verbose_name_plural": "Profiles Utilisateurs",
            },
        ),
    ]
