# Generated by Django 4.1.4 on 2023-03-14 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dict', '0002_historicalmeaning_dictionary_meaning_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalmeaning',
            old_name='dictionary_meaning',
            new_name='lemma_related',
        ),
        migrations.RenameField(
            model_name='meaning',
            old_name='dictionary_meaning',
            new_name='lemma_related',
        ),
    ]