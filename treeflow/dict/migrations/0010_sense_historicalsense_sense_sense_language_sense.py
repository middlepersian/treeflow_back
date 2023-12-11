# Generated by Django 4.2.7 on 2023-11-06 11:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models
import uuid


def migrate_meaning_to_sense(apps, schema_editor):
    # Get the model from the historical version
    Meaning = apps.get_model('dict', 'Meaning')
    Sense = apps.get_model('dict', 'Sense')
    # Migrate data from Meaning to Sense
    for meaning in Meaning.objects.all():
        # Create a Sense instance for each Meaning instance
        Sense.objects.create(
            id=meaning.id,
            sense=meaning.meaning,  # Replace 'meaning_text' with the actual field name in your Meaning model
            lemma_related=meaning.lemma_related,
            language=meaning.language,
            created_at=meaning.created_at,
            stage=meaning.stage
        )


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dict', '0009_remove_lemma_dict_lemma_word_ac16a5_idx_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sense',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('sense', models.TextField(blank=True, db_index=True, null=True)),
                ('lemma_related', models.BooleanField(default=True)),
                ('language', models.CharField(blank=True, db_index=True, max_length=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('stage', models.CharField(blank=True, max_length=10)),
                ('related_senses', models.ManyToManyField(blank=True, related_name='sense_related_senses', to='dict.sense')),
            ],
            options={
                'ordering': ['sense'],
            },
        ),
        migrations.CreateModel(
            name='HistoricalSense',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('sense', models.TextField(blank=True, db_index=True, null=True)),
                ('lemma_related', models.BooleanField(default=True)),
                ('language', models.CharField(blank=True, db_index=True, max_length=10, null=True)),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('stage', models.CharField(blank=True, max_length=10)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical sense',
                'verbose_name_plural': 'historical senses',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.AddConstraint(
            model_name='sense',
            constraint=models.UniqueConstraint(fields=('sense', 'language'), name='sense_language_sense'),
        ),
        # Add the RunPython operation here
        migrations.RunPython(migrate_meaning_to_sense),
    ]