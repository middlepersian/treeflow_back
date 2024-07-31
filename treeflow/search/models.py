import uuid
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField


class SearchCriteria(models.Model):
    QUERY_TYPE_CHOICES = [
        ("exact", "Exact"),
        ("contains", "Contains"),
        ("startswith", "Prefix"),
        ("endswith", "Suffix"),
        ("regex", "Regex"),
    ]

    FIELD_CHOICES = [
        ("id", "ID"),
        ("transcription", "Transcription"),
        ("transliteration", "Transliteration"),
        ("avestan", "Avestan"),
        ("gloss", "Gloss"),
        ("lemmas__word", "Lemma"),
        ("senses__sense", "Sense"),
        ("pos_token__pos", "POS"),
        ("feature_token__feature_value", "Feature without type"),
        ("comment_token__comment", "Comment"),
        ("comment_token__uncertain", "Uncertain"),
        ("comment_token__to_discuss", "To discuss"),
        ("comment_token__new_suggestion", "New suggestion"),
        ("text__series", "Sigle"),
        # ("created_at", "Created"),
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
    root = models.BooleanField(blank=False, default=False)
    language = models.CharField(blank=True, choices=LANGUAGE_CHOICES, default="")

    case_sensitive = models.BooleanField(blank=False, default=False)

    distance = models.PositiveIntegerField(blank=True, null=True, default=1)
    distance_type = models.CharField(
        blank=True,
        choices=DISTANCE_TYPE_CHOICES,
        default="both",
    )

    logical_operator = models.CharField(
        blank=True,
        choices=[("AND", "AND"), ("OR", "OR"), ("NOT", "NOT")],
        default="AND",
    )

