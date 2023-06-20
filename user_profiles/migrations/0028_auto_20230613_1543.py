# Generated by Django 3.2.13 on 2023-06-13 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profiles', '0027_remove_userprofile_controls'),
    ]

    operations = [
        migrations.RunSQL(
            "DROP TABLE public.filer_clipboard CASCADE"
        ),
        migrations.RunSQL(
            "DROP TABLE public.filer_clipboarditem CASCADE"
        ),
        migrations.RunSQL(
            "DROP TABLE public.filer_file CASCADE"
        ),
        migrations.RunSQL(
            "DROP TABLE public.filer_folder CASCADE"
        ),
        migrations.RunSQL(
            "DROP TABLE public.filer_folderpermission CASCADE"
        ),
        migrations.RunSQL(
            "DROP TABLE public.filer_image CASCADE"
        ),
        migrations.RunSQL(
            "DROP TABLE public.filer_thumbnailoption CASCADE"
        ),
        migrations.RunSQL(
            "DROP TABLE public.easy_thumbnails_source CASCADE"
        ),
        migrations.RunSQL(
            "DROP TABLE public.easy_thumbnails_thumbnail CASCADE"
        ),
        migrations.RunSQL(
            "DROP TABLE public.easy_thumbnails_thumbnaildimensions CASCADE"
        ),
    ]