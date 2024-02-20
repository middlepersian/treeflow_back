# Generated by Django 4.2.7 on 2024-02-15 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0030_token_corpus_toke_id_f4fc96_idx'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='section',
            index=models.Index(fields=['type', 'text'], name='corpus_sect_type_6c30d1_idx'),
        ),
    ]
