# Generated by Django 2.1.7 on 2019-06-05 14:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("control", "0023_auto_20190523_1712"),
    ]

    operations = [
        migrations.AlterField(
            model_name="questionnaire",
            name="order",
            field=models.PositiveIntegerField(db_index=True, verbose_name="order"),
        ),
    ]
