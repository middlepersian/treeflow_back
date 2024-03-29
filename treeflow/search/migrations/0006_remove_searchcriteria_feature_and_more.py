# Generated by Django 4.2.7 on 2023-12-07 12:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('corpus', '0022_remove_section_corpus_sect_text_id_567c68_idx_and_more'),
        ('search', '0005_rename_lemma_value_searchcriteria_lemma_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='searchcriteria',
            name='feature',
        ),
        migrations.RemoveField(
            model_name='searchcriteria',
            name='feature_type',
        ),
        migrations.RemoveField(
            model_name='searchcriteria',
            name='lemma',
        ),
        migrations.RemoveField(
            model_name='searchcriteria',
            name='lemma_language',
        ),
        migrations.RemoveField(
            model_name='searchcriteria',
            name='pos',
        ),
        migrations.RemoveField(
            model_name='searchcriteria',
            name='remove_stopwords',
        ),
        migrations.RemoveField(
            model_name='searchcriteria',
            name='sense',
        ),
        migrations.RemoveField(
            model_name='searchcriteria',
            name='sense_language',
        ),
        migrations.AddField(
            model_name='searchcriteria',
            name='logical_operator',
            field=models.CharField(choices=[('AND', 'AND'), ('OR', 'OR')], default='AND'),
        ),
        migrations.AddField(
            model_name='searchcriteria',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='searchcriteria',
            name='distance_type',
            field=models.CharField(choices=[('both', 'Both'), ('left', 'Left'), ('right', 'Right')], default='both'),
        ),
        migrations.AlterField(
            model_name='searchcriteria',
            name='query_field',
            field=models.CharField(choices=[('id', 'ID'), ('number', 'Number'), ('numberInSentence', 'Number in sentence'), ('root', 'Root'), ('text', 'Text'), ('language', 'Language'), ('transcription', 'Transcription'), ('transliteration', 'Transliteration'), ('avestan', 'Avestan'), ('gloss', 'Gloss'), ('created_at', 'Created')], default='transcription'),
        ),
        migrations.CreateModel(
            name='ResultFilter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remove_stopwords', models.BooleanField(default=False)),
                ('section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='corpus.section')),
                ('text', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='corpus.text')),
            ],
        ),
    ]
