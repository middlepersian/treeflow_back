# Generated by Django 3.1.13 on 2021-09-02 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codex', '0012_auto_20210902_1320'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicaltoken',
            old_name='trascription',
            new_name='transcription',
        ),
        migrations.RenameField(
            model_name='token',
            old_name='trascription',
            new_name='transcription',
        ),
    ]
