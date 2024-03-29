# Generated by Django 4.1.4 on 2023-02-21 20:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dict', '0001_initial'),
        ('images', '0001_initial'),
        ('corpus', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalcomment',
            name='image',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='images.image'),
        ),
        migrations.AddField(
            model_name='historicalcomment',
            name='lemma',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='dict.lemma'),
        ),
        migrations.AddField(
            model_name='historicalcomment',
            name='meaning',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='dict.meaning'),
        ),
        migrations.AddField(
            model_name='historicalcomment',
            name='section',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='corpus.section'),
        ),
        migrations.AddField(
            model_name='historicalcomment',
            name='semantic',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='dict.semantic'),
        ),
        migrations.AddField(
            model_name='historicalcomment',
            name='source',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='corpus.source'),
        ),
        migrations.AddField(
            model_name='historicalcomment',
            name='text',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='corpus.text'),
        ),
        migrations.AddField(
            model_name='historicalcomment',
            name='token',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='corpus.token'),
        ),
        migrations.AddField(
            model_name='historicalbibentry',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='feature',
            name='pos',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feature_pos', to='corpus.pos'),
        ),
        migrations.AddField(
            model_name='feature',
            name='token',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feature_token', to='corpus.token'),
        ),
        migrations.AddField(
            model_name='dependency',
            name='head',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dependency_head', to='corpus.token'),
        ),
        migrations.AddField(
            model_name='dependency',
            name='token',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dependency_token', to='corpus.token'),
        ),
        migrations.AddConstraint(
            model_name='corpus',
            constraint=models.UniqueConstraint(fields=('name', 'slug'), name='corpus_name_slug'),
        ),
        migrations.AddField(
            model_name='comment',
            name='dependency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_dependency', to='corpus.dependency'),
        ),
        migrations.AddField(
            model_name='comment',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_image', to='images.image'),
        ),
        migrations.AddField(
            model_name='comment',
            name='lemma',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_lemma', to='dict.lemma'),
        ),
        migrations.AddField(
            model_name='comment',
            name='meaning',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_meaning', to='dict.meaning'),
        ),
        migrations.AddField(
            model_name='comment',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_section', to='corpus.section'),
        ),
        migrations.AddField(
            model_name='comment',
            name='semantic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dict.semantic'),
        ),
        migrations.AddField(
            model_name='comment',
            name='source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_source', to='corpus.source'),
        ),
        migrations.AddField(
            model_name='comment',
            name='text',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_text', to='corpus.text'),
        ),
        migrations.AddField(
            model_name='comment',
            name='token',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_token', to='corpus.token'),
        ),
        migrations.AddIndex(
            model_name='tokenmeaning',
            index=models.Index(fields=['token'], name='corpus_toke_token_i_462ddf_idx'),
        ),
        migrations.AddIndex(
            model_name='tokenmeaning',
            index=models.Index(fields=['meaning'], name='corpus_toke_meaning_66123e_idx'),
        ),
        migrations.AddIndex(
            model_name='tokenmeaning',
            index=models.Index(fields=['token', 'meaning'], name='corpus_toke_token_i_bba668_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='tokenmeaning',
            unique_together={('token', 'meaning')},
        ),
        migrations.AddIndex(
            model_name='tokenlemma',
            index=models.Index(fields=['token'], name='corpus_toke_token_i_b49467_idx'),
        ),
        migrations.AddIndex(
            model_name='tokenlemma',
            index=models.Index(fields=['lemma'], name='corpus_toke_lemma_i_b732cc_idx'),
        ),
        migrations.AddIndex(
            model_name='tokenlemma',
            index=models.Index(fields=['token', 'lemma'], name='corpus_toke_token_i_08ee55_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='tokenlemma',
            unique_together={('token', 'lemma')},
        ),
        migrations.AddIndex(
            model_name='token',
            index=models.Index(fields=['text', 'number', 'transcription', 'transliteration', 'previous'], name='corpus_toke_text_id_f8c2b3_idx'),
        ),
        migrations.AddIndex(
            model_name='token',
            index=models.Index(fields=['text'], name='corpus_toke_text_id_0746ea_idx'),
        ),
        migrations.AddIndex(
            model_name='token',
            index=models.Index(fields=['previous'], name='corpus_toke_previou_94cf9a_idx'),
        ),
        migrations.AddIndex(
            model_name='token',
            index=models.Index(fields=['number'], name='corpus_toke_number_d42f91_idx'),
        ),
        migrations.AddIndex(
            model_name='token',
            index=models.Index(fields=['transcription'], name='corpus_toke_transcr_016958_idx'),
        ),
        migrations.AddIndex(
            model_name='token',
            index=models.Index(fields=['transliteration'], name='corpus_toke_transli_203651_idx'),
        ),
        migrations.AddConstraint(
            model_name='token',
            constraint=models.UniqueConstraint(fields=('number', 'text'), name='token_number_text'),
        ),
        migrations.AddConstraint(
            model_name='text',
            constraint=models.UniqueConstraint(fields=('corpus', 'identifier'), name='text_corpus_identifier'),
        ),
        migrations.AddIndex(
            model_name='source',
            index=models.Index(fields=['type', 'identifier'], name='corpus_sour_type_a9ba7b_idx'),
        ),
        migrations.AddConstraint(
            model_name='source',
            constraint=models.UniqueConstraint(fields=('type', 'identifier'), name='source_type_identifier'),
        ),
        migrations.AddIndex(
            model_name='sectiontoken',
            index=models.Index(fields=['section'], name='corpus_sect_section_aa3b63_idx'),
        ),
        migrations.AddIndex(
            model_name='sectiontoken',
            index=models.Index(fields=['token'], name='corpus_sect_token_i_b1fd0a_idx'),
        ),
        migrations.AddIndex(
            model_name='sectiontoken',
            index=models.Index(fields=['section', 'token'], name='corpus_sect_section_782af8_idx'),
        ),
        migrations.AddIndex(
            model_name='section',
            index=models.Index(fields=['text', 'number', 'identifier', 'previous', 'type', 'container'], name='corpus_sect_text_id_8e7c31_idx'),
        ),
        migrations.AddIndex(
            model_name='section',
            index=models.Index(fields=['text'], name='corpus_sect_text_id_8700f4_idx'),
        ),
        migrations.AddIndex(
            model_name='section',
            index=models.Index(fields=['number'], name='corpus_sect_number_4da742_idx'),
        ),
        migrations.AddIndex(
            model_name='section',
            index=models.Index(fields=['identifier'], name='corpus_sect_identif_d7915e_idx'),
        ),
        migrations.AddIndex(
            model_name='section',
            index=models.Index(fields=['previous'], name='corpus_sect_previou_f5dffe_idx'),
        ),
        migrations.AddIndex(
            model_name='section',
            index=models.Index(fields=['container'], name='corpus_sect_contain_c82f95_idx'),
        ),
        migrations.AddIndex(
            model_name='section',
            index=models.Index(fields=['type'], name='corpus_sect_type_49ae9a_idx'),
        ),
        migrations.AddConstraint(
            model_name='section',
            constraint=models.UniqueConstraint(fields=('text', 'identifier'), name='section_text_identifier'),
        ),
        migrations.AddIndex(
            model_name='pos',
            index=models.Index(fields=['token', 'pos', 'type'], name='corpus_pos_token_i_56eacc_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='pos',
            unique_together={('token', 'pos')},
        ),
        migrations.AddIndex(
            model_name='feature',
            index=models.Index(fields=['token', 'pos', 'feature', 'feature_value'], name='corpus_feat_token_i_c7cb40_idx'),
        ),
        migrations.AddIndex(
            model_name='dependency',
            index=models.Index(fields=['token', 'head', 'rel'], name='corpus_depe_token_i_3bd777_idx'),
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['text', 'token', 'lemma', 'meaning', 'semantic', 'dependency', 'image', 'section', 'source'], name='corpus_comm_text_id_b4e3c9_idx'),
        ),
    ]
