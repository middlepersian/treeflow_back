# Generated by Django 3.1.13 on 2022-03-28 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0006_auto_20220328_1727'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='corpus',
            name='corpus_name_slug',
        ),
    ]
