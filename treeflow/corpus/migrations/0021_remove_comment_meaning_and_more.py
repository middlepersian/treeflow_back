# Generated by Django 4.2.7 on 2023-11-07 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0020_comment_sense_historicalcomment_sense_section_senses'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='meaning',
        ),
        migrations.RemoveField(
            model_name='historicalcomment',
            name='meaning',
        ),
        migrations.RemoveField(
            model_name='section',
            name='meanings',
        ),
        migrations.DeleteModel(
            name='TokenMeaning',
        ),
    ]
