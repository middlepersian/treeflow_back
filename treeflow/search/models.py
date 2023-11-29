from django.db import models


class SearchCriteria(models.Model):
    QUERY_TYPE_CHOICES = [
        ("exact", "Exact"),
        ("fuzzy", "Fuzzy"),
    ]

    FIELD_CHOICES = [
        ("transcription", "Transcription"),
        ("transliteration", "Transliteration"),
        ("gloss", "Gloss"),
        ("avestan", "Avestan"),
        ("language", "Language"),
        ("root", "Root"),
        ("number", "Number"),
        ("numberInSentence", "Number In Sentence"),
        ("id", "ID"),
        ("text", "Text"),
    ]

    LANGUAGE_CHOICES = [
        ("", "All"),
        ("Middle_Persian", "Middle Persian"),
        ("Imperial_Aramaic", "Imperial Aramaic"),
        ("Avestan", "Avestan"),
        ("Ancient_Greek", "Ancient Greek"),
        ("Parthian", "Parthian"),
        ("Parsi", "Parsi"),
        ("Arabic", "Arabic"),
        ("Gujarati", "Gujarati"),
        ("Sanskrit", "Sanskrit"),
        ("English", "English"),
        ("French", "French"),
        ("German", "German"),
        ("Italian", "Italian"),
        ("Spanish", "Spanish"),
    ]

    query_type = models.CharField(
        max_length=20, choices=QUERY_TYPE_CHOICES, default="exact"
    )

    query_field = models.CharField(
        max_length=20, choices=FIELD_CHOICES, default="transcription"
    )

    query_value = models.CharField(max_length=255, default="")

    pos_token = models.CharField(max_length=255, blank=True, default="")

    remove_stopwords = models.BooleanField(default=False)

    distance = models.IntegerField(blank=True, null=True, default=0)

    feature = models.CharField(max_length=255, blank=True, default="")

    feature_value = models.CharField(max_length=255, blank=True, default="")

    lemma_language = models.CharField(
        max_length=20, blank=True, choices=LANGUAGE_CHOICES, default=""
    )

    lemma_value = models.CharField(max_length=255, blank=True, default="")

    meaning_language = models.CharField(
        max_length=20, blank=True, choices=LANGUAGE_CHOICES, default=""
    )

    meaning_value = models.CharField(max_length=255, blank=True, default="")
