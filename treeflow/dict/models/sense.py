import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from treeflow.utils.normalize import strip_and_normalize



class Sense(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    sense = models.TextField(null=True, blank=True, db_index=True)
    lemma_related = models.BooleanField(default=True)
    language = models.CharField(max_length=15, blank=True, null=True, db_index=True)
    related_senses = models.ManyToManyField('self', blank=True, related_name='sense_related_senses')
    created_at = models.DateTimeField(auto_now_add=True)
    stage = models.CharField(max_length=10, blank=True)

    def related_lemmas(self):
            return self.lemma_related_senses.all()
            
    history = HistoricalRecords()
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['sense', 'language'], name='sense_language_sense'
            )]
        ordering = ['sense']

    def __str__(self):
        return '{} - {} - {}'.format(self.sense, self.language, self.lemma_related)

    def save(self, *args, **kwargs):
        # Normalize only the `normalized_field` before saving
        self.sense = strip_and_normalize('NFC', self.sense)
        #process language
        self.language = self.language.strip().lower()
        super().save(*args, **kwargs)