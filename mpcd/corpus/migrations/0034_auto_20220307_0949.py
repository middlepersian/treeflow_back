# Generated by Django 3.1.13 on 2022-03-07 08:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('corpus', '0033_auto_20220221_2008'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalMorphologicalAnnotation',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('feature', models.CharField(blank=True, max_length=10, null=True)),
                ('feature_value', models.CharField(blank=True, max_length=10, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical morphological annotation',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.DeleteModel(
            name='Feature',
        ),
        migrations.DeleteModel(
            name='FeatureValue',
        ),
        migrations.DeleteModel(
            name='Pos',
        ),
        migrations.AlterField(
            model_name='historicaltext',
            name='title',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='historicaltoken',
            name='pos',
            field=models.CharField(blank=True, choices=[('ADJ', 'ADJ'), ('ADP', 'ADP'), ('ADV', 'ADV'), ('AUX', 'AUX'), ('CCONJ', 'CCONJ'), ('DET', 'DET'), ('INTJ', 'INTJ'), ('NOUN', 'NOUN'), ('NUM', 'NUM'), ('PART', 'PART'), ('PRON', 'PRON'), ('PROPN', 'PROPN'), ('PUNCT', 'PUNCT'), ('SCONJ', 'SCONJ'), ('SYM', 'SYM'), ('VERB', 'VERB'), ('X', 'X')], max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='text',
            name='title',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='token',
            name='pos',
            field=models.CharField(blank=True, choices=[('ADJ', 'ADJ'), ('ADP', 'ADP'), ('ADV', 'ADV'), ('AUX', 'AUX'), ('CCONJ', 'CCONJ'), ('DET', 'DET'), ('INTJ', 'INTJ'), ('NOUN', 'NOUN'), ('NUM', 'NUM'), ('PART', 'PART'), ('PRON', 'PRON'), ('PROPN', 'PROPN'), ('PUNCT', 'PUNCT'), ('SCONJ', 'SCONJ'), ('SYM', 'SYM'), ('VERB', 'VERB'), ('X', 'X')], max_length=8, null=True),
        ),
    ]
