# Generated by Django 3.1.13 on 2021-09-02 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codex', '0009_auto_20210902_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='features',
            field=models.ManyToManyField(blank=True, to='codex.MorphologicalAnnotation'),
        ),
    ]
