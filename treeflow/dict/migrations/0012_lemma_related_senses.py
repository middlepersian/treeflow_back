# Generated by Django 4.2.7 on 2023-11-07 09:06

from django.db import migrations, models



def populate_related_senses(apps, schema_editor):
    Lemma = apps.get_model('dict', 'Lemma')
    Sense = apps.get_model('dict', 'Sense')
    LemmaSense = apps.get_model('dict', 'LemmaSense')  # Get the through model

    for lemma in Lemma.objects.all():
        # Get the related meanings for this lemma
        lemma_meanings = lemma.related_meanings.all()

        # For each related meaning, find or create a corresponding Sense and associate it
        for meaning in lemma_meanings:
            sense, created = Sense.objects.get_or_create(
                sense=meaning.meaning,  # Assuming a 'meaning' field exists in Sense for matching
                language=meaning.language,
            )
            # Now, create the association in LemmaSense for the lemma and the found/created sense
            LemmaSense.objects.get_or_create(
                lemma=lemma,
                sense=sense
            )

class Migration(migrations.Migration):

    dependencies = [
        ('dict', '0011_lemmasense_historicallemmasense_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lemma',
            name='related_senses',
            field=models.ManyToManyField(blank=True, related_name='lemma_related_senses', through='dict.LemmaSense', to='dict.sense'),
        ),
        migrations.RunPython(populate_related_senses),
    ]
