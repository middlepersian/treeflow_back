# Generated by Django 3.1.13 on 2021-09-07 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codex', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chapter',
            old_name='text_id',
            new_name='text',
        ),
        migrations.RenameField(
            model_name='codextoken',
            old_name='line_id',
            new_name='line',
        ),
        migrations.RenameField(
            model_name='historicalchapter',
            old_name='text_id',
            new_name='text',
        ),
        migrations.RenameField(
            model_name='historicalcodextoken',
            old_name='line_id',
            new_name='line',
        ),
        migrations.RenameField(
            model_name='historicalline',
            old_name='description',
            new_name='comment',
        ),
        migrations.RenameField(
            model_name='historicalline',
            old_name='side_id',
            new_name='side',
        ),
        migrations.RenameField(
            model_name='historicalsection',
            old_name='chapter_id',
            new_name='chapter',
        ),
        migrations.RenameField(
            model_name='historicalsentence',
            old_name='section_id',
            new_name='section',
        ),
        migrations.RenameField(
            model_name='historicalstrophe',
            old_name='text_id',
            new_name='text',
        ),
        migrations.RenameField(
            model_name='historicaltext',
            old_name='codex_id',
            new_name='codex',
        ),
        migrations.RenameField(
            model_name='historicalverse',
            old_name='verse_id',
            new_name='verse',
        ),
        migrations.RenameField(
            model_name='line',
            old_name='description',
            new_name='comment',
        ),
        migrations.RenameField(
            model_name='line',
            old_name='side_id',
            new_name='side',
        ),
        migrations.RenameField(
            model_name='section',
            old_name='chapter_id',
            new_name='chapter',
        ),
        migrations.RenameField(
            model_name='sentence',
            old_name='section_id',
            new_name='section',
        ),
        migrations.RenameField(
            model_name='strophe',
            old_name='text_id',
            new_name='text',
        ),
        migrations.RenameField(
            model_name='text',
            old_name='codex_id',
            new_name='codex',
        ),
        migrations.RenameField(
            model_name='verse',
            old_name='verse_id',
            new_name='verse',
        ),
        migrations.RemoveField(
            model_name='folio',
            name='description',
        ),
        migrations.RemoveField(
            model_name='historicalfolio',
            name='description',
        ),
        migrations.RemoveField(
            model_name='historicalside',
            name='description',
        ),
        migrations.RemoveField(
            model_name='side',
            name='description',
        ),
        migrations.AddField(
            model_name='folio',
            name='comment',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='historicalfolio',
            name='comment',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='historicalside',
            name='comment',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='side',
            name='comment',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='codex',
            name='description',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='folio',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='historicalcodex',
            name='description',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='historicalfolio',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
