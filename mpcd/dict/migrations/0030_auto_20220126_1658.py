# Generated by Django 3.1.13 on 2022-01-26 15:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dict', '0029_auto_20220126_1255'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HistoricalWord',
            new_name='HistoricalLemma',
        ),
        migrations.AlterModelOptions(
            name='historicallemma',
            options={'get_latest_by': 'history_date', 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical lemma'},
        ),
        migrations.CreateModel(
            name='Lemma',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('word', models.CharField(max_length=100, unique=True)),
                ('language', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lemma_language', to='dict.language')),
            ],
        ),
        migrations.AlterField(
            model_name='entry',
            name='lemma',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='entry_lemma', to='dict.lemma'),
        ),
        migrations.AlterField(
            model_name='historicalentry',
            name='lemma',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='dict.lemma'),
        ),
        migrations.DeleteModel(
            name='Word',
        ),
    ]
