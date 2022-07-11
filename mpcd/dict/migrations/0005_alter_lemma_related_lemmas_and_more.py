# Generated by Django 4.0.6 on 2022-07-11 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dict', '0004_auto_20220711_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lemma',
            name='related_lemmas',
            field=models.ManyToManyField(blank=True, related_name='lemma_related_lemmas', to='dict.lemma'),
        ),
        migrations.AlterField(
            model_name='meaning',
            name='related_meanings',
            field=models.ManyToManyField(blank=True, related_name='meaning_related_meanings', to='dict.meaning'),
        ),
        migrations.AlterField(
            model_name='semantic',
            name='related_semantics',
            field=models.ManyToManyField(blank=True, related_name='semantic_related_semantics', to='dict.semantic'),
        ),
    ]
