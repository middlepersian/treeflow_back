# Generated by Django 4.2.7 on 2024-02-07 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0020_rename_is_root_searchcriteria_root'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='searchsession',
            name='formset',
        ),
        migrations.AddField(
            model_name='searchsession',
            name='filters',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
