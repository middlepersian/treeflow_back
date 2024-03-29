# Generated by Django 4.2.7 on 2023-12-06 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0004_rename_field_searchcriteria_query_field_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='searchcriteria',
            old_name='lemma_value',
            new_name='lemma',
        ),
        migrations.RenameField(
            model_name='searchcriteria',
            old_name='pos_token',
            new_name='pos',
        ),
        migrations.RenameField(
            model_name='searchcriteria',
            old_name='query_value',
            new_name='query',
        ),
        migrations.RenameField(
            model_name='searchcriteria',
            old_name='meaning_value',
            new_name='sense',
        ),
        migrations.RemoveField(
            model_name='searchcriteria',
            name='feature_value',
        ),
        migrations.RemoveField(
            model_name='searchcriteria',
            name='meaning_language',
        ),
        migrations.AddField(
            model_name='searchcriteria',
            name='distance_type',
            field=models.CharField(blank=True, default='both'),
        ),
        migrations.AddField(
            model_name='searchcriteria',
            name='feature_type',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='searchcriteria',
            name='sense_language',
            field=models.CharField(blank=True, choices=[('', 'All'), ('pal', 'Middle Persian'), ('arc', 'Imperial Aramaic'), ('ave', 'Avestan'), ('grc', 'Ancient Greek'), ('xpr', 'Parthian'), ('prp', 'Parsi'), ('ara', 'Arabic'), ('guj', 'Gujarati'), ('san', 'Sanskrit'), ('eng', 'English'), ('fra', 'French'), ('deu', 'German'), ('ita', 'Italian'), ('spa', 'Spanish')], default=''),
        ),
        migrations.AlterField(
            model_name='searchcriteria',
            name='lemma_language',
            field=models.CharField(blank=True, choices=[('', 'All'), ('pal', 'Middle Persian'), ('arc', 'Imperial Aramaic'), ('ave', 'Avestan'), ('grc', 'Ancient Greek'), ('xpr', 'Parthian'), ('prp', 'Parsi'), ('ara', 'Arabic'), ('guj', 'Gujarati'), ('san', 'Sanskrit'), ('eng', 'English'), ('fra', 'French'), ('deu', 'German'), ('ita', 'Italian'), ('spa', 'Spanish')], default=''),
        ),
        migrations.AlterField(
            model_name='searchcriteria',
            name='query_field',
            field=models.CharField(choices=[('id', 'ID'), ('number', 'Number'), ('numberInSentence', 'Number in sentence'), ('root', 'Root'), ('text', 'Text'), ('language', 'Language'), ('transcription', 'Transcription'), ('transliteration', 'Transliteration'), ('avestan', 'Avestan'), ('gloss', 'Gloss'), ('created_at', 'Created')], default='id'),
        ),
        migrations.AlterField(
            model_name='searchcriteria',
            name='query_type',
            field=models.CharField(choices=[('exact', 'Exact'), ('fuzzy', 'Fuzzy')], default='exact'),
        ),
    ]
