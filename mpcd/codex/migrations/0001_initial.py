# Generated by Django 3.1.13 on 2021-09-01 10:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dict', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Codex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dependency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('head', models.PositiveSmallIntegerField()),
                ('rel', models.CharField(choices=[('acl', 'clausal modifier of noun (adnominal clause)'), ('advcl', 'adverbial clause modifier'), ('advmod', 'adverbial modifier'), ('amod', 'adjectival modifier'), ('appos', 'appositional modifier'), ('aux', 'auxiliary'), ('case', 'case marking'), ('cc', 'coordinating conjunction'), ('ccomp', 'clausal complement'), ('compound', 'compound'), ('conj', 'conjunct'), ('cop', 'copula'), ('det', 'determiner'), ('discourse', 'discourse element'), ('fixed', 'fixed multiword expression'), ('iobj', 'indirect object'), ('mark', 'marker'), ('nmod', 'nominal modifier'), ('nsubj', 'nominal subject'), ('nummod', 'numeric modifier'), ('obj', 'object'), ('obl', 'oblique nominal'), ('root', 'root')], max_length=9)),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=20, unique=True)),
                ('value', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='FeatureValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.SlugField(unique=True)),
                ('value', models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Folio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True)),
                ('codex_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codex.codex')),
            ],
        ),
        migrations.CreateModel(
            name='MorphologicalAnnotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('pos', models.CharField(choices=[('ADJ', 'Adjective'), ('ADP', 'Adposition'), ('ADV', 'Adverb'), ('AUX', 'Auxiliary'), ('CCONJ', 'Coordinating conjunction'), ('DET', 'Determiner'), ('INTJ', 'Interjection'), ('NOUN', 'Noun'), ('NUM', 'Numeral'), ('PART', 'Particle'), ('PRON', 'Pronoun'), ('PROPN', 'Proper noun'), ('PUNCT', 'Punctuation'), ('SCONJO', 'Subordinating conjunction'), ('SYM', 'Symbol'), ('VERB', 'Verb'), ('X', 'Other')], max_length=6, null=True)),
                ('feature', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='codex.feature')),
                ('feature_value', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='codex.featurevalue')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('chapter_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codex.chapter')),
            ],
        ),
        migrations.CreateModel(
            name='Strophe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='SyntacticAnnotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('dependency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='codex.dependency')),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('token', models.CharField(max_length=50)),
                ('trascription', models.CharField(blank=True, max_length=50)),
                ('transliteration', models.CharField(blank=True, max_length=50)),
                ('comment', models.TextField(blank=True)),
                ('avestan', models.CharField(blank=True, max_length=255)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TokenSemantics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('meaning', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CodexToken',
            fields=[
                ('token_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='codex.token')),
            ],
            bases=('codex.token',),
        ),
        migrations.CreateModel(
            name='Verse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('tokens', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lyric_tokens', to='codex.token')),
                ('verse_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codex.strophe')),
            ],
        ),
        migrations.CreateModel(
            name='TokenUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='token',
            name='changed_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='codex.tokenuser'),
        ),
        migrations.AddField(
            model_name='token',
            name='lemma',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dict.entry'),
        ),
        migrations.AddField(
            model_name='token',
            name='morph_annotations',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='codex.morphologicalannotation'),
        ),
        migrations.AddField(
            model_name='token',
            name='syntax_annotations',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='codex.syntacticannotation'),
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_type', models.CharField(choices=[('P', 'Prose'), ('L', 'Lyric')], max_length=1)),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('codex_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codex.codex')),
            ],
        ),
        migrations.AddField(
            model_name='strophe',
            name='text_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codex.text'),
        ),
        migrations.CreateModel(
            name='Side',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True)),
                ('folio_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codex.folio')),
            ],
        ),
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('section_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codex.section')),
                ('tokens', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prose_tokens', to='codex.token')),
            ],
        ),
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True)),
                ('side_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codex.side')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalToken',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('token', models.CharField(max_length=50)),
                ('trascription', models.CharField(blank=True, max_length=50)),
                ('transliteration', models.CharField(blank=True, max_length=50)),
                ('comment', models.TextField(blank=True)),
                ('avestan', models.CharField(blank=True, max_length=255)),
                ('pub_date', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('changed_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='codex.tokenuser')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='codex.tokenuser')),
                ('lemma', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='dict.entry')),
                ('morph_annotations', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='codex.morphologicalannotation')),
                ('syntax_annotations', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='codex.syntacticannotation')),
            ],
            options={
                'verbose_name': 'historical token',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.AddConstraint(
            model_name='featurevalue',
            constraint=models.UniqueConstraint(fields=('name', 'value'), name='featurevalue_name_value'),
        ),
        migrations.AddConstraint(
            model_name='feature',
            constraint=models.UniqueConstraint(fields=('name', 'value'), name='feature_name_value'),
        ),
        migrations.AddConstraint(
            model_name='dependency',
            constraint=models.CheckConstraint(check=models.Q(rel__in=['acl', 'advcl', 'advmod', 'amod', 'appos', 'aux', 'case', 'cc', 'ccomp', 'compound', 'conj', 'cop', 'det', 'discourse', 'fixed', 'iobj', 'mark', 'nmod', 'nsubj', 'nummod', 'obj', 'obl', 'root']), name='valid_rel'),
        ),
        migrations.AddConstraint(
            model_name='dependency',
            constraint=models.UniqueConstraint(fields=('head', 'rel'), name='head_rel'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='text_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codex.text'),
        ),
        migrations.AddConstraint(
            model_name='morphologicalannotation',
            constraint=models.CheckConstraint(check=models.Q(pos__in=['ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM', 'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJO', 'SYM', 'VERB', 'X']), name='valid_pos'),
        ),
        migrations.AddConstraint(
            model_name='morphologicalannotation',
            constraint=models.UniqueConstraint(fields=('pos', 'feature', 'feature_value'), name='pos_feature_feature_value'),
        ),
        migrations.AddField(
            model_name='codextoken',
            name='line_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codex.line'),
        ),
    ]
