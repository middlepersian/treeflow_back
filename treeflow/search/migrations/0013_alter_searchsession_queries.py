# Generated by Django 4.2.7 on 2023-12-18 10:45

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0012_alter_searchsession_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchsession',
            name='queries',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, default=''), blank=True, null=True, size=None),
        ),
    ]
