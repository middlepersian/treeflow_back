# Generated by Django 3.1.13 on 2021-09-02 08:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codex', '0002_auto_20210902_1003'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feature',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='featurevalue',
            options={'ordering': ('name',)},
        ),
    ]
