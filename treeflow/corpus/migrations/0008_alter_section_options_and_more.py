# Generated by Django 4.1.4 on 2023-03-06 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0007_alter_tokenlemma_lemma_alter_tokenlemma_token_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='section',
            options={'ordering': ['created_at']},
        ),
        migrations.AddIndex(
            model_name='section',
            index=models.Index(fields=['created_at'], name='corpus_sect_created_9eb0a0_idx'),
        ),
    ]
