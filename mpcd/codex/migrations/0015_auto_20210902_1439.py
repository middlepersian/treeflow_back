# Generated by Django 3.1.13 on 2021-09-02 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codex', '0014_codextoken_line_position'),
    ]

    operations = [
        migrations.RenameField(
            model_name='codextoken',
            old_name='line_position',
            new_name='position',
        ),
    ]
