# Generated by Django 4.2.7 on 2024-02-29 07:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0034_remove_token_corpus_toke_id_f4fc96_idx_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalcomment',
            name='dependency',
        ),
        migrations.RemoveField(
            model_name='historicalcomment',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalcomment',
            name='image',
        ),
        migrations.RemoveField(
            model_name='historicalcomment',
            name='lemma',
        ),
        migrations.RemoveField(
            model_name='historicalcomment',
            name='section',
        ),
        migrations.RemoveField(
            model_name='historicalcomment',
            name='semantic',
        ),
        migrations.RemoveField(
            model_name='historicalcomment',
            name='sense',
        ),
        migrations.RemoveField(
            model_name='historicalcomment',
            name='source',
        ),
        migrations.RemoveField(
            model_name='historicalcomment',
            name='text',
        ),
        migrations.RemoveField(
            model_name='historicalcomment',
            name='token',
        ),
        migrations.RemoveField(
            model_name='historicalcomment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='historicalcorpus',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaldependency',
            name='head',
        ),
        migrations.RemoveField(
            model_name='historicaldependency',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaldependency',
            name='token',
        ),
        migrations.RemoveField(
            model_name='historicalfeature',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalfeature',
            name='pos',
        ),
        migrations.RemoveField(
            model_name='historicalfeature',
            name='token',
        ),
        migrations.RemoveField(
            model_name='historicalpos',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalpos',
            name='token',
        ),
        migrations.RemoveField(
            model_name='historicalsection',
            name='container',
        ),
        migrations.RemoveField(
            model_name='historicalsection',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalsection',
            name='previous',
        ),
        migrations.RemoveField(
            model_name='historicalsection',
            name='source',
        ),
        migrations.RemoveField(
            model_name='historicalsection',
            name='text',
        ),
        migrations.RemoveField(
            model_name='historicalsource',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaltext',
            name='corpus',
        ),
        migrations.RemoveField(
            model_name='historicaltext',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaltoken',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaltoken',
            name='image',
        ),
        migrations.RemoveField(
            model_name='historicaltoken',
            name='previous',
        ),
        migrations.RemoveField(
            model_name='historicaltoken',
            name='text',
        ),
        migrations.DeleteModel(
            name='HistoricalBibEntry',
        ),
        migrations.DeleteModel(
            name='HistoricalComment',
        ),
        migrations.DeleteModel(
            name='HistoricalCorpus',
        ),
        migrations.DeleteModel(
            name='HistoricalDependency',
        ),
        migrations.DeleteModel(
            name='HistoricalFeature',
        ),
        migrations.DeleteModel(
            name='HistoricalPOS',
        ),
        migrations.DeleteModel(
            name='HistoricalSection',
        ),
        migrations.DeleteModel(
            name='HistoricalSource',
        ),
        migrations.DeleteModel(
            name='HistoricalText',
        ),
        migrations.DeleteModel(
            name='HistoricalToken',
        ),
    ]