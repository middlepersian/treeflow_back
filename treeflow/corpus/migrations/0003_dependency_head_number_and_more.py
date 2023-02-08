# Generated by Django 4.1.4 on 2023-02-08 14:11

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dependency',
            name='head_number',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicaldependency',
            name='head_number',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='historicaltoken',
            name='number_in_sentence',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(blank=True, null=True), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='token',
            name='number_in_sentence',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(blank=True, null=True), blank=True, null=True, size=None),
        ),
    ]
