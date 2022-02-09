# Generated by Django 3.1.13 on 2022-02-09 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0009_auto_20220204_0931'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalsentence',
            name='number',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalsentence',
            name='previous',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='corpus.sentence'),
        ),
        migrations.AddField(
            model_name='sentence',
            name='number',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sentence',
            name='previous',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='next', to='corpus.sentence'),
        ),
    ]
