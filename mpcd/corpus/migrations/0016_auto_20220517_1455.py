# Generated by Django 3.1.13 on 2022-05-17 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0015_auto_20220509_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaltoken',
            name='pos',
            field=models.CharField(blank=True, choices=[('ADJ', 'adjective'), ('ADP', 'adposition'), ('ADV', 'adverb'), ('AUX', 'auxiliary'), ('CCONJ', 'coordinating conjunction'), ('DET', 'determiner'), ('INTJ', 'interjection'), ('NOUN', 'noun'), ('NUM', 'numeral'), ('PART', 'particle'), ('PRON', 'pronoun'), ('PROPN', 'proper noun'), ('PUNCT', 'punctuation'), ('SCONJ', 'subordinating conjunction'), ('SYM', 'symbol'), ('VERB', 'verb'), ('X', 'other')], max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='token',
            name='pos',
            field=models.CharField(blank=True, choices=[('ADJ', 'adjective'), ('ADP', 'adposition'), ('ADV', 'adverb'), ('AUX', 'auxiliary'), ('CCONJ', 'coordinating conjunction'), ('DET', 'determiner'), ('INTJ', 'interjection'), ('NOUN', 'noun'), ('NUM', 'numeral'), ('PART', 'particle'), ('PRON', 'pronoun'), ('PROPN', 'proper noun'), ('PUNCT', 'punctuation'), ('SCONJ', 'subordinating conjunction'), ('SYM', 'symbol'), ('VERB', 'verb'), ('X', 'other')], max_length=8, null=True),
        ),
    ]
