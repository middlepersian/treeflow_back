# Generated by Django 4.1.4 on 2023-03-16 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dict', '0003_rename_dictionary_meaning_historicalmeaning_lemma_related_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicallemma',
            name='category',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='lemma',
            name='category',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
