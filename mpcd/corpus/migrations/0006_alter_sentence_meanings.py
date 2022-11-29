# Generated by Django 4.1.2 on 2022-11-29 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dict', '0002_alter_historicaldictionary_options_and_more'),
        ('corpus', '0005_rename_translations_sentence_meanings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentence',
            name='meanings',
            field=models.ManyToManyField(related_name='sentence_meanings', to='dict.meaning'),
        ),
    ]
