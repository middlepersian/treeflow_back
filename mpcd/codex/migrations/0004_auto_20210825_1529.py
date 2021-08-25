# Generated by Django 3.1.13 on 2021-08-25 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codex', '0003_auto_20210825_1526'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='morphologicalannotation',
            constraint=models.CheckConstraint(check=models.Q(pos__in=['ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM', 'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJO', 'SYM', 'VERB', 'X']), name='codex_morphologicalannotation_pos_valid'),
        ),
    ]
