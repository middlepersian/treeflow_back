# Generated by Django 3.1.13 on 2022-01-12 08:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dict', '0027_auto_20220103_1642'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='BibEntry',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('year', models.PositiveSmallIntegerField()),
                ('url', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Corpus',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dependency',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('head', models.PositiveSmallIntegerField()),
                ('rel', models.CharField(choices=[('acl', 'clausal modifier of noun (adnominal clause)'), ('advcl', 'adverbial clause modifier'), ('advmod', 'adverbial modifier'), ('amod', 'adjectival modifier'), ('appos', 'appositional modifier'), ('aux', 'auxiliary'), ('case', 'case marking'), ('cc', 'coordinating conjunction'), ('ccomp', 'clausal complement'), ('compound', 'compound'), ('conj', 'conjunct'), ('cop', 'copula'), ('det', 'determiner'), ('discourse', 'discourse element'), ('fixed', 'fixed multiword expression'), ('iobj', 'indirect object'), ('mark', 'marker'), ('nmod', 'nominal modifier'), ('nsubj', 'nominal subject'), ('nummod', 'numeric modifier'), ('obj', 'object'), ('obl', 'oblique nominal'), ('root', 'root')], max_length=9)),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='FeatureValue',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Folio',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('comment', models.CharField(blank=True, max_length=255)),
            ],
        ),
       
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('number', models.IntegerField()),
                ('comment', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='MorphologicalAnnotation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Pos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pos', models.CharField(choices=[('ADJ', 'ADJ'), ('ADP', 'ADP'), ('ADV', 'ADV'), ('AUX', 'AUX'), ('CCONJ', 'CCONJ'), ('DET', 'DET'), ('INTJ', 'INTJ'), ('NOUN', 'NOUN'), ('NUM', 'NUM'), ('PART', 'PART'), ('PRON', 'PRON'), ('PROPN', 'PROPN'), ('PUNCT', 'PUNCT'), ('SCONJO', 'SCONJO'), ('SYM', 'SYM'), ('VERB', 'VERB'), ('X', 'X')], max_length=6, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('project', models.TextField(blank=True, null=True)),
                ('reference', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('translation', models.TextField(blank=True, null=True)),
                ('comment', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, null=True, unique=True)),
                ('slug', models.SlugField(max_length=10, unique=True)),
                ('description', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('stage', models.CharField(blank=True, choices=[('UNT', 'untouched'), ('PRO', 'in_progress'), ('FIN', 'finished')], default='UNT', max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='TextSigle',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('sigle', models.CharField(choices=[('AM', 'AM'), ('AOD', 'AŌD'), ('Aog', 'Aog'), ('ASS', 'ASS'), ('AWM', 'AWM'), ('AWN', 'AWN'), ('AZ', 'AZ'), ('CHP', 'CHP'), ('DA', 'DA'), ('Dd', 'Dd'), ('Dk3', 'Dk3'), ('Dk4', 'Dk4'), ('Dk5', 'Dk5'), ('Dk6', 'Dk6'), ('Dk7', 'Dk7'), ('Dk8', 'Dk8'), ('Dk9', 'Dk9'), ('DkC', 'DkC'), ('DMX', 'DMX'), ('ENN', 'ENN'), ('GA', 'GA'), ('GBd', 'GBd'), ('Her', 'Hēr'), ('HKR', 'HKR'), ('HN', 'HN'), ('IndBd', 'IndBd'), ('KAP', 'KAP'), ('MFRH', 'MFRH'), ('MHD', 'MHD'), ('MK_Andarz', 'MK-Andarz'), ('MYFr', 'MYFr'), ('N', 'N'), ('NM', 'NM'), ('OHD', 'OHD'), ('P', 'P'), ('PahlRivDd', 'PahlRivDd'), ('PT', 'PT'), ('PV', 'PV'), ('PY', 'PY'), ('RAF', 'RAF'), ('REA', 'RĒA'), ('SGW', 'ŠGW'), ('SiE', 'ŠiĒ'), ('SnS', 'ŠnŠ'), ('Vr', 'Vr'), ('Vyt', 'Vyt'), ('WCNA', 'WCNA'), ('WD', 'WD'), ('WDWM', 'WDWM'), ('WZ', 'WZ'), ('XD', 'X&D'), ('XAv', 'XAv'), ('ZFJ', 'ZFJ'), ('ZWY', 'ZWY')], max_length=10, unique=True)),
                ('genre', models.CharField(choices=[('ZAN', 'zand'), ('PTE', 'PT-epitomes'), ('PTR', 'PT-reworking'), ('TEO', 'theological'), ('AUT', 'authorial-th'), ('JUR', 'jur'), ('AND', 'andarz'), ('NAR', 'narrative')], max_length=3, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('transcription', models.CharField(max_length=50)),
                ('transliteration', models.CharField(blank=True, max_length=50)),
                ('comment', models.TextField(blank=True)),
                ('avestan', models.URLField(blank=True, max_length=100, null=True)),
                ('lemma', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='token_lemma', to='dict.entry')),
                ('morphological_annotation', models.ManyToManyField(blank=True, related_name='token_morphological_annotation', to='corpus.MorphologicalAnnotation')),
                ('pos', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='corpus.pos')),
                ('previous', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='token_previous', to='corpus.token')),
                ('syntactic_annotation', models.ManyToManyField(blank=True, related_name='token_syntactic_annotation', to='corpus.Dependency')),
            ],
        ),
        migrations.CreateModel(
            name='Codex',
            fields=[
                ('source_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='corpus.source')),
                ('sigle', models.CharField(choices=[('MK', 'MK'), ('TD1', 'TD1'), ('TD4a', 'TD4a'), ('DH6', 'DH6'), ('BK', 'BK'), ('TD2', 'TD2'), ('MJ', 'Minocher Jamaspji62(Dd)'), ('IOL', 'IOL CCXXVIII (PRDd)'), ('B', 'B'), ('P', 'P'), ('M51', 'M51'), ('K20', 'K20'), ('K20b', 'K20b'), ('K27', 'K27'), ('K35', 'K35'), ('K43a', 'K43a'), ('K43b', 'K43b'), ('K26', 'K26'), ('msMHD', 'MS of MHD')], default='', max_length=10, unique=True)),
                ('copy_date', models.TextField(blank=True, null=True)),
                ('copy_place_name', models.CharField(blank=True, max_length=100, null=True)),
                ('copy_place_latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('copy_place_longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('library', models.CharField(blank=True, max_length=100)),
                ('signature', models.CharField(blank=True, max_length=100)),
            ],
            bases=('corpus.source',),
        ),
        migrations.CreateModel(
            name='CodexToken',
            fields=[
                ('token_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='corpus.token')),
                ('position', models.PositiveSmallIntegerField(null=True)),
            ],
            bases=('corpus.token',),
        ),
        migrations.CreateModel(
            name='Edition',
            fields=[
                ('source_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='corpus.source')),
            ],
            bases=('corpus.source',),
        ),
         migrations.CreateModel(
            name='HistoricalCodex',
            fields=[
                ('source_ptr', models.ForeignKey(auto_created=True, blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, parent_link=True, related_name='+', to='corpus.source')),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('name', models.CharField(db_index=True, max_length=100, null=True)),
                ('slug', models.SlugField(max_length=10)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('sigle', models.CharField(choices=[('MK', 'MK'), ('TD1', 'TD1'), ('TD4a', 'TD4a'), ('DH6', 'DH6'), ('BK', 'BK'), ('TD2', 'TD2'), ('MJ', 'Minocher Jamaspji62(Dd)'), ('IOL', 'IOL CCXXVIII (PRDd)'), ('B', 'B'), ('P', 'P'), ('M51', 'M51'), ('K20', 'K20'), ('K20b', 'K20b'), ('K27', 'K27'), ('K35', 'K35'), ('K43a', 'K43a'), ('K43b', 'K43b'), ('K26', 'K26'), ('msMHD', 'MS of MHD')], db_index=True, default='', max_length=10)),
                ('copy_date', models.TextField(blank=True, null=True)),
                ('copy_place_name', models.CharField(blank=True, max_length=100, null=True)),
                ('copy_place_latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('copy_place_longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('library', models.CharField(blank=True, max_length=100)),
                ('signature', models.CharField(blank=True, max_length=100)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical codex',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalCodexToken',
            fields=[
                ('token_ptr', models.ForeignKey(auto_created=True, blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, parent_link=True, related_name='+', to='corpus.token')),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('transcription', models.CharField(max_length=50)),
                ('transliteration', models.CharField(blank=True, max_length=50)),
                ('comment', models.TextField(blank=True)),
                ('avestan', models.URLField(blank=True, max_length=100, null=True)),
                ('position', models.PositiveSmallIntegerField(null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical codex token',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalCorpus',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('slug', models.SlugField(max_length=10)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical corpus',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalEdition',
            fields=[
                ('source_ptr', models.ForeignKey(auto_created=True, blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, parent_link=True, related_name='+', to='corpus.source')),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('name', models.CharField(db_index=True, max_length=100, null=True)),
                ('slug', models.SlugField(max_length=10)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical edition',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalFolio',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('name', models.CharField(max_length=100)),
                ('comment', models.CharField(blank=True, max_length=255)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical folio',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalLine',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('number', models.IntegerField()),
                ('comment', models.TextField(blank=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical line',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSentence',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('translation', models.TextField(blank=True, null=True)),
                ('comment', models.CharField(blank=True, max_length=255)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical sentence',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSource',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('name', models.CharField(db_index=True, max_length=100, null=True)),
                ('slug', models.SlugField(max_length=10)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical source',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalText',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('title', models.CharField(max_length=100)),
                ('stage', models.CharField(blank=True, choices=[('UNT', 'untouched'), ('PRO', 'in_progress'), ('FIN', 'finished')], default='UNT', max_length=3)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical text',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalToken',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('transcription', models.CharField(max_length=50)),
                ('transliteration', models.CharField(blank=True, max_length=50)),
                ('comment', models.TextField(blank=True)),
                ('avestan', models.URLField(blank=True, max_length=100, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical token',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.AddConstraint(
            model_name='textsigle',
            constraint=models.CheckConstraint(check=models.Q(sigle__in=['AM', 'AOD', 'Aog', 'ASS', 'AWM', 'AWN', 'AZ', 'CHP', 'DA', 'Dd', 'Dk3', 'Dk4', 'Dk5', 'Dk6', 'Dk7', 'Dk8', 'Dk9', 'DkC', 'DMX', 'ENN', 'GA', 'GBd', 'Her', 'HKR', 'HN', 'IndBd', 'KAP', 'MFRH', 'MHD', 'MK_Andarz', 'MYFr', 'N', 'NM', 'OHD', 'P', 'PahlRivDd', 'PT', 'PV', 'PY', 'RAF', 'REA', 'SGW', 'SiE', 'SnS', 'Vr', 'Vyt', 'WCNA', 'WD', 'WDWM', 'WZ', 'XD', 'XAv', 'ZFJ', 'ZWY']), name='valid_sigle'),
        ),
        migrations.AddConstraint(
            model_name='textsigle',
            constraint=models.CheckConstraint(check=models.Q(genre__in=['ZAN', 'PTE', 'PTR', 'TEO', 'AUT', 'JUR', 'AND', 'NAR']), name='valid_genre'),
        ),
        migrations.AddConstraint(
            model_name='textsigle',
            constraint=models.UniqueConstraint(fields=('sigle', 'genre'), name='sigle_genre'),
        ),
        migrations.AddField(
            model_name='text',
            name='collaborators',
            field=models.ManyToManyField(blank=True, related_name='text_collaborators', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='text',
            name='corpus',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='corpus.corpus'),
        ),
        migrations.AddField(
            model_name='text',
            name='editors',
            field=models.ManyToManyField(blank=True, related_name='text_editors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='text',
            name='resources',
            field=models.ManyToManyField(blank=True, to='corpus.Resource'),
        ),
        migrations.AddField(
            model_name='text',
            name='sources',
            field=models.ManyToManyField(blank=True, to='corpus.Source'),
        ),
        migrations.AddField(
            model_name='text',
            name='text_sigle',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='corpus.textsigle'),
        ),
        migrations.AddField(
            model_name='sentence',
            name='text',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='corpus.text'),
        ),
        migrations.AddField(
            model_name='sentence',
            name='tokens',
            field=models.ManyToManyField(to='corpus.Token'),
        ),
        migrations.AddField(
            model_name='resource',
            name='authors',
            field=models.ManyToManyField(blank=True, related_name='resource_authors', to='corpus.Author'),
        ),
        migrations.AddConstraint(
            model_name='pos',
            constraint=models.CheckConstraint(check=models.Q(pos__in=['ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM', 'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJO', 'SYM', 'VERB', 'X']), name='valid_pos'),
        ),
        migrations.AddField(
            model_name='morphologicalannotation',
            name='feature',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='corpus.feature'),
        ),
        migrations.AddField(
            model_name='morphologicalannotation',
            name='feature_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='corpus.featurevalue'),
        ),
        migrations.AddField(
            model_name='line',
            name='side',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='corpus.folio'),
        ),
        migrations.AddField(
            model_name='historicaltoken',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicaltoken',
            name='lemma',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='dict.entry'),
        ),
        migrations.AddField(
            model_name='historicaltoken',
            name='pos',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='corpus.pos'),
        ),
        migrations.AddField(
            model_name='historicaltoken',
            name='previous',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='corpus.token'),
        ),
        migrations.AddField(
            model_name='historicaltext',
            name='corpus',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='corpus.corpus'),
        ),
        migrations.AddField(
            model_name='historicaltext',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicaltext',
            name='text_sigle',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='corpus.textsigle'),
        ),
        migrations.AddField(
            model_name='historicalsource',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalsentence',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalsentence',
            name='text',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='corpus.text'),
        ),
        migrations.AddField(
            model_name='historicalline',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalline',
            name='side',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='corpus.folio'),
        ),
        migrations.AddField(
            model_name='historicalfolio',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicaledition',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalcorpus',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalcodextoken',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalcodextoken',
            name='lemma',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='dict.entry'),
        ),
        migrations.AddField(
            model_name='historicalcodextoken',
            name='line',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='corpus.line'),
        ),
        migrations.AddField(
            model_name='historicalcodextoken',
            name='pos',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='corpus.pos'),
        ),
        migrations.AddField(
            model_name='historicalcodextoken',
            name='previous',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='corpus.token'),
        ),
        migrations.AddField(
            model_name='historicalcodex',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
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
            model_name='bibentry',
            name='authors',
            field=models.ManyToManyField(related_name='bib_entry_authors', to='corpus.Author'),
        ),
        migrations.AddConstraint(
            model_name='author',
            constraint=models.UniqueConstraint(fields=('name', 'last_name'), name='name_lastname'),
        ),
        migrations.AddConstraint(
            model_name='text',
            constraint=models.CheckConstraint(check=models.Q(stage__in=['UNT', 'PRO', 'FIN']), name='valid_stage'),
        ),
        migrations.AddConstraint(
            model_name='morphologicalannotation',
            constraint=models.UniqueConstraint(fields=('feature', 'feature_value'), name='feature_featurevalue'),
        ),
        migrations.AddField(
            model_name='historicalfolio',
            name='codex',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='corpus.codex'),
        ),
        migrations.AddField(
            model_name='folio',
            name='codex',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corpus.codex'),
        ),
        migrations.AddField(
            model_name='edition',
            name='authors',
            field=models.ManyToManyField(blank=True, related_name='edition_authors', to='corpus.Author'),
        ),
        migrations.AddField(
            model_name='edition',
            name='references',
            field=models.ManyToManyField(blank=True, related_name='edition_references', to='corpus.BibEntry'),
        ),
        migrations.AddField(
            model_name='edition',
            name='text_sigle',
            field=models.ManyToManyField(blank=True, related_name='edition_text_sigles', to='corpus.TextSigle'),
        ),
        migrations.AddField(
            model_name='codextoken',
            name='line',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corpus.line'),
        ),
        migrations.AddField(
            model_name='codex',
            name='facsimile',
            field=models.ManyToManyField(blank=True, related_name='codex_facsimile', to='corpus.BibEntry'),
        ),
        migrations.AddField(
            model_name='codex',
            name='scribe',
            field=models.ManyToManyField(blank=True, related_name='codex_scribe', to='corpus.Author'),
        ),
    ]
