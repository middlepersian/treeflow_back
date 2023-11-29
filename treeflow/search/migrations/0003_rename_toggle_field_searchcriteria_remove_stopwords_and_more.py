# Generated by Django 4.2.7 on 2023-11-27 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0002_rename_searchform_searchcriteria'),
    ]

    operations = [
        migrations.RenameField(
            model_name='searchcriteria',
            old_name='toggle_field',
            new_name='remove_stopwords',
        ),
        migrations.RemoveField(
            model_name='searchcriteria',
            name='criteria_scope',
        ),
        migrations.RemoveField(
            model_name='searchcriteria',
            name='criteria_value',
        ),
        migrations.RemoveField(
            model_name='searchcriteria',
            name='lemmas_word',
        ),
        migrations.RemoveField(
            model_name='searchcriteria',
            name='search_input',
        ),
        migrations.AddField(
            model_name='searchcriteria',
            name='distance',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='searchcriteria',
            name='feature',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='searchcriteria',
            name='feature_value',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='searchcriteria',
            name='field',
            field=models.CharField(choices=[('transcription', 'Transcription'), ('transliteration', 'Transliteration'), ('gloss', 'Gloss'), ('avestan', 'Avestan'), ('language', 'Language'), ('root', 'Root'), ('number', 'Number'), ('numberInSentence', 'Number In Sentence'), ('id', 'ID'), ('text', 'Text')], default='transcription', max_length=20),
        ),
        migrations.AddField(
            model_name='searchcriteria',
            name='lemma_language',
            field=models.CharField(choices=[('', 'All'), ('Middle_Persian', 'Middle Persian'), ('Imperial_Aramaic', 'Imperial Aramaic'), ('Avestan', 'Avestan'), ('Ancient_Greek', 'Ancient Greek'), ('Parthian', 'Parthian'), ('Parsi', 'Parsi'), ('Arabic', 'Arabic'), ('Gujarati', 'Gujarati'), ('Sanskrit', 'Sanskrit'), ('English', 'English'), ('French', 'French'), ('German', 'German'), ('Italian', 'Italian'), ('Spanish', 'Spanish')], default='', max_length=20),
        ),
        migrations.AddField(
            model_name='searchcriteria',
            name='lemma_word',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='searchcriteria',
            name='meaning_language',
            field=models.CharField(choices=[('', 'All'), ('Middle_Persian', 'Middle Persian'), ('Imperial_Aramaic', 'Imperial Aramaic'), ('Avestan', 'Avestan'), ('Ancient_Greek', 'Ancient Greek'), ('Parthian', 'Parthian'), ('Parsi', 'Parsi'), ('Arabic', 'Arabic'), ('Gujarati', 'Gujarati'), ('Sanskrit', 'Sanskrit'), ('English', 'English'), ('French', 'French'), ('German', 'German'), ('Italian', 'Italian'), ('Spanish', 'Spanish')], default='', max_length=20),
        ),
        migrations.AddField(
            model_name='searchcriteria',
            name='meaning_word',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='searchcriteria',
            name='pos_token',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='searchcriteria',
            name='query_type',
            field=models.CharField(choices=[('exact', 'Exact'), ('fuzzy', 'Fuzzy')], default='exact', max_length=20),
        ),
        migrations.AddField(
            model_name='searchcriteria',
            name='value',
            field=models.CharField(default='', max_length=255),
        ),
    ]
