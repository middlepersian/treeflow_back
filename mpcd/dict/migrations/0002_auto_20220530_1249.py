# Generated by Django 3.1.13 on 2022-05-30 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dict', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='definition',
            name='language',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='dictionary',
            name='source_languages',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='historicaldefinition',
            name='language',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='historicaldictionary',
            name='source_languages',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='historicalmeaning',
            name='language',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='meaning',
            name='language',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]