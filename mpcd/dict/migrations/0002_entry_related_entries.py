# Generated by Django 3.1.13 on 2022-02-08 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dict', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='related_entries',
            field=models.ManyToManyField(blank=True, related_name='_entry_related_entries_+', to='dict.Entry'),
        ),
    ]