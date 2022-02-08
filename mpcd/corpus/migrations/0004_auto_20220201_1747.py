# Generated by Django 3.1.13 on 2022-02-01 16:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0003_auto_20220131_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalsection',
            name='source',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='corpus.source'),
        ),
        migrations.AddField(
            model_name='section',
            name='source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='section_source', to='corpus.source'),
        ),
    ]