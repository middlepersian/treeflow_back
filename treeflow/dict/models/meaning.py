import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from treeflow.utils.normalize import strip_and_normalize



class Meaning(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    meaning = models.TextField(null=True, blank=True, db_index=True)
    lemma_related = models.BooleanField(default=True)
    language = models.CharField(max_length=10, blank=True, null=True, db_index=True)
    related_meanings = models.ManyToManyField('self', blank=True, related_name='meaning_related_meanings')
    created_at = models.DateTimeField(auto_now_add=True)


    def related_lemmas(self):
            return self.lemma_related_meanings.all()
            
    history = HistoricalRecords()
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['meaning', 'language'], name='meaning_language_meaning'
            )]
        ordering = ['meaning']
        indexes = [
            models.Index(fields=['meaning', 'language']),
        ]

    def __str__(self):
        return '{} - {} - {}'.format(self.meaning, self.language, self.lemma_related)

    def save(self, *args, **kwargs):
        # Normalize only the `normalized_field` before saving
        self.meaning = strip_and_normalize('NFC', self.meaning)
        #process language
        self.language = self.language.strip().lower()
        super().save(*args, **kwargs)