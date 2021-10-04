# Generated by Django 3.1.13 on 2021-10-04 08:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dict', '0010_auto_20211002_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='category',
            field=models.ManyToManyField(blank=True, to='dict.Category'),
        ),
        migrations.AddField(
            model_name='entry',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='definition',
            field=models.ManyToManyField(blank=True, to='dict.Definition'),
        ),
        migrations.AddField(
            model_name='entry',
            name='literature',
            field=models.ManyToManyField(blank=True, to='dict.Reference'),
        ),
        migrations.AddField(
            model_name='entry',
            name='loanword',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dict.loanword'),
        ),
        migrations.AddField(
            model_name='entry',
            name='translation',
            field=models.ManyToManyField(blank=True, to='dict.Translation'),
        ),
        migrations.AddField(
            model_name='historicalentry',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalentry',
            name='loanword',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='dict.loanword'),
        ),
    ]
