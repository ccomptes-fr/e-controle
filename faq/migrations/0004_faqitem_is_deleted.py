# Generated by Django 3.2.18 on 2023-11-11 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0003_faqitem_deleted_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='faqitem',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
