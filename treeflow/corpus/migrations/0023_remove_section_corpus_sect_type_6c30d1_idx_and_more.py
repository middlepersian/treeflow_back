# Generated by Django 4.2.7 on 2023-12-01 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0022_remove_section_corpus_sect_text_id_567c68_idx_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='section',
            name='corpus_sect_type_6c30d1_idx',
        ),
        migrations.AddIndex(
            model_name='section',
            index=models.Index(fields=['type', 'text', 'identifier'], name='corpus_sect_type_775d9b_idx'),
        ),
    ]