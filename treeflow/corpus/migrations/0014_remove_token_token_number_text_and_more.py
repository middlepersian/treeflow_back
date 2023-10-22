# Generated by Django 4.2.2 on 2023-10-22 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0013_dependency_enhanced_historicaldependency_enhanced'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='token',
            name='token_number_text',
        ),
        migrations.RemoveIndex(
            model_name='comment',
            name='corpus_comm_text_id_b4e3c9_idx',
        ),
        migrations.RemoveIndex(
            model_name='dependency',
            name='corpus_depe_token_i_3bd777_idx',
        ),
        migrations.RemoveIndex(
            model_name='feature',
            name='corpus_feat_token_i_c7cb40_idx',
        ),
        migrations.RemoveIndex(
            model_name='pos',
            name='corpus_pos_token_i_56eacc_idx',
        ),
        migrations.RemoveIndex(
            model_name='section',
            name='corpus_sect_text_id_8e7c31_idx',
        ),
        migrations.RemoveIndex(
            model_name='section',
            name='corpus_sect_text_id_8700f4_idx',
        ),
        migrations.RemoveIndex(
            model_name='section',
            name='corpus_sect_number_4da742_idx',
        ),
        migrations.RemoveIndex(
            model_name='section',
            name='corpus_sect_identif_d7915e_idx',
        ),
        migrations.RemoveIndex(
            model_name='section',
            name='corpus_sect_previou_f5dffe_idx',
        ),
        migrations.RemoveIndex(
            model_name='section',
            name='corpus_sect_contain_c82f95_idx',
        ),
        migrations.RemoveIndex(
            model_name='section',
            name='corpus_sect_type_49ae9a_idx',
        ),
        migrations.RemoveIndex(
            model_name='section',
            name='corpus_sect_created_9eb0a0_idx',
        ),
        migrations.RemoveIndex(
            model_name='source',
            name='corpus_sour_type_a9ba7b_idx',
        ),
        migrations.RemoveIndex(
            model_name='token',
            name='corpus_toke_text_id_f8c2b3_idx',
        ),
        migrations.RemoveIndex(
            model_name='token',
            name='corpus_toke_text_id_0746ea_idx',
        ),
        migrations.RemoveIndex(
            model_name='token',
            name='corpus_toke_previou_94cf9a_idx',
        ),
        migrations.RemoveIndex(
            model_name='tokenlemma',
            name='corpus_toke_token_i_08ee55_idx',
        ),
        migrations.RemoveIndex(
            model_name='tokenmeaning',
            name='corpus_toke_token_i_bba668_idx',
        ),
        migrations.AlterUniqueTogether(
            name='pos',
            unique_together=set(),
        ),
        migrations.AddIndex(
            model_name='section',
            index=models.Index(fields=['text', 'type'], name='corpus_sect_text_id_567c68_idx'),
        ),
        migrations.AddConstraint(
            model_name='token',
            constraint=models.UniqueConstraint(fields=('text', 'number'), name='token_text_number'),
        ),
    ]
