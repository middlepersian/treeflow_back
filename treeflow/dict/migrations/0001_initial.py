# Generated by Django 4.1.4 on 2023-02-08 09:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dictionary',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('source_languages', models.CharField(blank=True, max_length=3, null=True)),
                ('slug', models.SlugField(max_length=10, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='HistoricalDictionary',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('source_languages', models.CharField(blank=True, max_length=3, null=True)),
                ('slug', models.SlugField(max_length=10)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical dictionary',
                'verbose_name_plural': 'historical dictionarys',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalLemma',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('word', models.CharField(max_length=100)),
                ('language', models.CharField(blank=True, max_length=3, null=True)),
                ('multiword_expression', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical lemma',
                'verbose_name_plural': 'historical lemmas',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalMeaning',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('meaning', models.TextField(blank=True, null=True)),
                ('language', models.CharField(blank=True, max_length=10, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical meaning',
                'verbose_name_plural': 'historical meanings',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSemantic',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical semantic',
                'verbose_name_plural': 'historical semantics',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalTermTech',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('category', models.CharField(choices=[('astr', 'astronomy'), ('bot', 'botany'), ('econom', 'economy'), ('geogr', 'geography'), ('legal', 'legal'), ('measure', 'measurement'), ('med', 'medicine'), ('myth', 'mythology'), ('philos', 'philosophy'), ('pol', 'politics'), ('purity', 'purity'), ('ritual', 'ritual'), ('theol', 'theology'), ('zool', 'zoology')], db_index=True, max_length=10)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical term tech',
                'verbose_name_plural': 'historical term techs',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Lemma',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('word', models.CharField(max_length=100)),
                ('language', models.CharField(blank=True, max_length=3, null=True)),
                ('multiword_expression', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['word'],
            },
        ),
        migrations.CreateModel(
            name='Meaning',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('meaning', models.TextField(blank=True, null=True)),
                ('language', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'ordering': ['meaning'],
            },
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('reference', models.CharField(blank=True, max_length=350, null=True, unique=True)),
                ('url', models.URLField(blank=True, null=True)),
            ],
            options={
                'ordering': ['reference'],
            },
        ),
        migrations.CreateModel(
            name='TermTech',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('category', models.CharField(choices=[('astr', 'astronomy'), ('bot', 'botany'), ('econom', 'economy'), ('geogr', 'geography'), ('legal', 'legal'), ('measure', 'measurement'), ('med', 'medicine'), ('myth', 'mythology'), ('philos', 'philosophy'), ('pol', 'politics'), ('purity', 'purity'), ('ritual', 'ritual'), ('theol', 'theology'), ('zool', 'zoology')], max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Semantic',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('lemmas', models.ManyToManyField(blank=True, related_name='semantic_lemmas', to='dict.lemma')),
                ('meanings', models.ManyToManyField(blank=True, related_name='semantic_meanings', to='dict.meaning')),
                ('related_semantics', models.ManyToManyField(blank=True, to='dict.semantic')),
                ('term_techs', models.ManyToManyField(blank=True, related_name='semantic_term_techs', to='dict.termtech')),
            ],
        ),
        migrations.AddConstraint(
            model_name='reference',
            constraint=models.UniqueConstraint(fields=('reference', 'url'), name='reference_url'),
        ),
        migrations.AddField(
            model_name='meaning',
            name='related_meanings',
            field=models.ManyToManyField(blank=True, to='dict.meaning'),
        ),
        migrations.AddField(
            model_name='lemma',
            name='related_lemmas',
            field=models.ManyToManyField(blank=True, to='dict.lemma'),
        ),
        migrations.AddField(
            model_name='lemma',
            name='related_meanings',
            field=models.ManyToManyField(blank=True, related_name='lemma_related_meanings', to='dict.meaning'),
        ),
        migrations.AddField(
            model_name='historicaltermtech',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalsemantic',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalmeaning',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicallemma',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicaldictionary',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='dictionary',
            constraint=models.UniqueConstraint(fields=('name', 'slug'), name='dictionary_name_slug'),
        ),
        migrations.AddConstraint(
            model_name='meaning',
            constraint=models.UniqueConstraint(fields=('meaning', 'language'), name='meaning_language_meaning'),
        ),
        migrations.AddConstraint(
            model_name='lemma',
            constraint=models.UniqueConstraint(fields=('word', 'language'), name='word_language_lemma'),
        ),
    ]
