# Generated by Django 4.2.7 on 2023-11-20 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SearchForm',
            new_name='SearchCriteria',
        ),
    ]
