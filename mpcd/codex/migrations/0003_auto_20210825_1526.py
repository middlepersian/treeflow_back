# Generated by Django 3.1.13 on 2021-08-25 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codex', '0002_auto_20210825_1306'),
    ]

    operations = [
        migrations.RenameField(
            model_name='morphologicalannotation',
            old_name='pos_tag',
            new_name='pos',
        ),
    ]
