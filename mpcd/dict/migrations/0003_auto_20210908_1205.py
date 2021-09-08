# Generated by Django 3.1.13 on 2021-09-08 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dict', '0002_auto_20210908_1144'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='year',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='category',
            field=models.ManyToManyField(blank=True, to='dict.Category'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='cross_reference',
            field=models.ManyToManyField(blank=True, related_name='entry_cross_reference', to='dict.Lemma'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='definition',
            field=models.ManyToManyField(blank=True, to='dict.Definition'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='literature',
            field=models.ManyToManyField(blank=True, to='dict.Reference'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='translation',
            field=models.ManyToManyField(blank=True, to='dict.Meaning'),
        ),
    ]
