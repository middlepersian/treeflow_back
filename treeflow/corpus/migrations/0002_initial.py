# Generated by Django 4.1.4 on 2023-02-10 09:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dict', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
            name='section_type',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='corpus.sectiontype'),
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
            model_name='historicalcomment',
            name='user',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalbibentry',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dependency',
            name='head',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dependency_head', to='corpus.token'),
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
            name='section_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_section_type', to='corpus.sectiontype'),
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
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='token',
            constraint=models.UniqueConstraint(fields=('number', 'text'), name='token_number_text'),
        ),
        migrations.AddConstraint(
            model_name='text',
            constraint=models.UniqueConstraint(fields=('corpus', 'title'), name='corpus_title'),
        ),
    ]
