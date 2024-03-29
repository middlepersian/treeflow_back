# Generated by Django 4.2.7 on 2023-11-06 11:42

from django.db import migrations, models
import django.db.models.deletion


def transfer_tokenmeanings_to_tokensenses(apps, schema_editor):
    # Get the models
    TokenMeaning = apps.get_model('corpus', 'TokenMeaning')
    TokenSense = apps.get_model('corpus', 'TokenSense')
    Sense = apps.get_model('dict', 'Sense')

    # Transfer data from TokenMeaning to TokenSense
    for token_meaning in TokenMeaning.objects.all():
        # Assuming you have the same ID in Sense as in Meaning,
        # get the corresponding Sense instance.
        # If they are not the same, you need a way to map them, possibly through another field.
        sense_instance = Sense.objects.get(id=token_meaning.meaning_id)

        # Create a new TokenSense instance with the same token and the new sense
        TokenSense.objects.create(
            token=token_meaning.token,
            sense=sense_instance,
            created_at=token_meaning.created_at  # Carry over the created_at timestamp if needed
        )

class Migration(migrations.Migration):

    dependencies = [
        ('dict', '0011_lemmasense_historicallemmasense_and_more'),
        ('corpus', '0017_alter_section_options_alter_sectiontoken_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='TokenSense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('sense', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dict.sense')),
                ('token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corpus.token')),
            ],
            options={
                'indexes': [models.Index(fields=['token'], name='corpus_toke_token_i_3eef13_idx'), models.Index(fields=['sense'], name='corpus_toke_sense_i_f1d425_idx')],
                'unique_together': {('token', 'sense')},
            },
        ),
        migrations.RunPython(transfer_tokenmeanings_to_tokensenses),
    ]
