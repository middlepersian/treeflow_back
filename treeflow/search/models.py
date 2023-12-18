import uuid
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField


class SearchCriteria(models.Model):
    # Options
    QUERY_TYPE_CHOICES = [
        ("exact", "Exact"),
        ("fuzzy", "Fuzzy"),
    ]

    FIELD_CHOICES = [
        ("id", "ID"),
        ("number", "Number"),
        ("numberInSentence", "Number in sentence"),
        ("root", "Root"),
        # ("text", "Text"),
        ("language", "Language"),
        ("transcription", "Transcription"),
        ("transliteration", "Transliteration"),
        ("avestan", "Avestan"),
        ("gloss", "Gloss"),
        ("created_at", "Created"),
    ]

    LANGUAGE_CHOICES = [
        ("", "All"),
        ("pal", "Middle Persian"),
        ("arc", "Imperial Aramaic"),
        ("ave", "Avestan"),
        ("grc", "Ancient Greek"),
        ("xpr", "Parthian"),
        ("prp", "Parsi"),
        ("ara", "Arabic"),
        ("guj", "Gujarati"),
        ("san", "Sanskrit"),
        ("eng", "English"),
        ("fra", "French"),
        ("deu", "German"),
        ("ita", "Italian"),
        ("spa", "Spanish"),
    ]

    DISTANCE_TYPE_CHOICES = [
        ("both", "On either side of anchor"),
        ("before", "Preceding anchor"),
        ("after", "Following anchor"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )

    query = models.CharField(blank=False, max_length=255, default="")
    query_type = models.CharField(
        blank=False, choices=QUERY_TYPE_CHOICES, default="exact"
    )
    query_field = models.CharField(
        blank=False, choices=FIELD_CHOICES, default="transcription"
    )

    distance = models.PositiveIntegerField(blank=True, null=True, default=0)
    distance_type = models.CharField(
        blank=True,
        choices=DISTANCE_TYPE_CHOICES,
        default="both",
    )

    logical_operator = models.CharField(
        blank=True,
        choices=[("AND", "AND"), ("OR", "OR")],
        default="AND",
    )

    # TODO: Missing fields
    # lemmas
    # senses
    # pos
    # features


class SearchSession(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, null=False, unique=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    session_id = models.CharField(max_length=255, null=True, blank=True)
    formset = models.ManyToManyField(SearchCriteria, blank=True)
    results = ArrayField(models.UUIDField(default=uuid.uuid4), null=True, blank=True)
    queries = ArrayField(models.CharField(blank=True, default=""), null=True, blank=True)

    class Meta:
        unique_together = (
            "user",
            "session_id",
            "queries",
        )


class ResultFilter(models.Model):
    text = models.ForeignKey(
        "corpus.Text", null=True, blank=True, on_delete=models.CASCADE
    )
    section = models.ForeignKey(
        "corpus.Section", null=True, blank=True, on_delete=models.CASCADE
    )
    remove_stopwords = models.BooleanField(default=False)
