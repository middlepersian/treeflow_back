import uuid as uuid_lib
from django.db import models
from django.contrib.postgres.fields import ArrayField
from treeflow.utils.normalize import strip_and_normalize


class Lemma(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    word = models.CharField(max_length=100)
    language = models.CharField(max_length=3, null=True, blank=True)
    categories = ArrayField(
         models.CharField(max_length=50, blank=True, null=True), null=True, blank=True
     )
    multiword_expression = models.BooleanField(default=False)
    related_lemmas = models.ManyToManyField(
        "self", blank=True, related_name="lemma_related_lemmas", through="LemmaRelation"
    )
    related_senses = models.ManyToManyField(
        "Sense",
        blank=True,
        related_name="lemma_related_senses",
        through="LemmaSense",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    stage = models.CharField(max_length=10, blank=True)


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["word", "language"], name="word_language_lemma"
            )
        ]
        ordering = ["word"]

    def save(self, *args, **kwargs):
        # Normalize only the `normalized_field` before saving
        self.word = strip_and_normalize("NFC", self.word)
        # process language
        if self.language:
            self.language = self.language.strip().lower()


        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return "{} - {}".format(self.word, self.language)


class LemmaRelation(models.Model):
    lemma1 = models.ForeignKey(
        Lemma, on_delete=models.CASCADE, related_name="related_lemmas1"
    )
    lemma2 = models.ForeignKey(
        Lemma, on_delete=models.CASCADE, related_name="related_lemmas2"
    )
    # eg hypernymy, hyponymy, meronymy, holonymy, synonymy, antonymy, etc.
    relation_type = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["lemma1", "lemma2"], name="lemma_relation")
        ]

class LemmaSense(models.Model):
    lemma = models.ForeignKey(
        Lemma, on_delete=models.CASCADE, related_name="related_lemma_sense"
    )
    sense = models.ForeignKey(
        "Sense", on_delete=models.CASCADE, related_name="related_sense"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["lemma", "sense"], name="lemma_sense")
        ]        