# Generated by Django 4.2.7 on 2023-11-29 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0021_remove_comment_meaning_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='section',
            name='corpus_sect_text_id_567c68_idx',
        ),
        migrations.AddIndex(
            model_name='section',
            index=models.Index(fields=['type', 'text'], name='corpus_sect_type_6c30d1_idx'),
        ),
        migrations.AddIndex(
            model_name='token',
            index=models.Index(fields=['text'], name='corpus_toke_text_id_0746ea_idx'),
        ),
    ]
