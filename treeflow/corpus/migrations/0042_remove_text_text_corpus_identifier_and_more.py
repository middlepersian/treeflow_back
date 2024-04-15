# Generated by Django 4.2.7 on 2024-04-15 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0041_alter_token_options_alter_bibentry_modified_at_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='text',
            name='text_corpus_identifier',
        ),
        migrations.AlterField(
            model_name='text',
            name='identifier',
            field=models.CharField(blank=True, db_index=True, max_length=20, null=True, unique=True),
        ),
    ]
