# Generated by Django 4.1.4 on 2023-07-10 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dict', '0006_remove_historicallemma_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicallemma',
            name='stage',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='historicalmeaning',
            name='stage',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='lemma',
            name='stage',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='meaning',
            name='stage',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
