# Generated by Django 4.1.4 on 2023-05-15 11:32

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dict', '0005_alter_historicallemma_category_alter_lemma_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicallemma',
            name='category',
        ),
        migrations.RemoveField(
            model_name='lemma',
            name='category',
        ),
        migrations.AddField(
            model_name='historicallemma',
            name='categories',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50, null=True), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='lemma',
            name='categories',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50, null=True), blank=True, null=True, size=None),
        ),
    ]