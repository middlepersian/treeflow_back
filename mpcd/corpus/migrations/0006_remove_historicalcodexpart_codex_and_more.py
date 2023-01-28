# Generated by Django 4.1.4 on 2023-01-28 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0005_remove_facsimile_codex_part_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalcodexpart',
            name='codex',
        ),
        migrations.RemoveField(
            model_name='historicalcodexpart',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='codex_part',
        ),
        migrations.RemoveField(
            model_name='historicalcomment',
            name='codex_part',
        ),
        migrations.AlterField(
            model_name='facsimile',
            name='codex',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='facsimile_codex', to='corpus.codex'),
        ),
        migrations.DeleteModel(
            name='CodexPart',
        ),
        migrations.DeleteModel(
            name='HistoricalCodexPart',
        ),
    ]
