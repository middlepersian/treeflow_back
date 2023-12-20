# Generated by Django 4.2.7 on 2023-11-07 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0021_remove_comment_meaning_and_more'),
        ('dict', '0012_lemma_related_senses'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalmeaning',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='lemmameaning',
            name='lemma',
        ),
        migrations.RemoveField(
            model_name='lemmameaning',
            name='meaning',
        ),
        migrations.RemoveField(
            model_name='meaning',
            name='related_meanings',
        ),
        migrations.RemoveField(
            model_name='lemma',
            name='related_meanings',
        ),
        migrations.DeleteModel(
            name='HistoricalLemmaMeaning',
        ),
        migrations.DeleteModel(
            name='HistoricalMeaning',
        ),
        migrations.DeleteModel(
            name='LemmaMeaning',
        ),
        migrations.DeleteModel(
            name='Meaning',
        ),
    ]
