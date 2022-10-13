# Generated by Django 4.0.6 on 2022-10-13 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0003_alter_historicalbibentry_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalsection',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='section',
            name='comment',
        ),
        migrations.AddField(
            model_name='section',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='section_comments', to='corpus.comment'),
        ),
    ]
