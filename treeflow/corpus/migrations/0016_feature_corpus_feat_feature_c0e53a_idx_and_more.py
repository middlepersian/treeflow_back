# Generated by Django 4.2.2 on 2023-10-27 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0015_section_corpus_sect_type_49ae9a_idx'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='feature',
            index=models.Index(fields=['feature', 'feature_value'], name='corpus_feat_feature_c0e53a_idx'),
        ),
        migrations.AddIndex(
            model_name='pos',
            index=models.Index(fields=['pos'], name='corpus_pos_pos_56620e_idx'),
        ),
    ]
