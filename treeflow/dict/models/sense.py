import uuid as uuid_lib
from django.db import models
from django.conf import settings
from django.utils import timezone
from treeflow.utils.normalize import strip_and_normalize



class Sense(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    sense = models.TextField(null=True, blank=True, db_index=True)
    lemma_related = models.BooleanField(default=True)
    language = models.CharField(max_length=3, blank=True, null=True, db_index=True)
    related_senses = models.ManyToManyField('self', blank=True, related_name='sense_related_senses')
    stage = models.CharField(max_length=10, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_senses')

    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='modified_senses',
        blank=True
    )


    def related_lemmas(self):
            return self.lemma_related_senses.all()
            
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['sense', 'language'], name='sense_language_sense'
            )]
        ordering = ['sense']

    def __str__(self):
        return '{} - {}'.format(self.sense, self.language)

    def save(self, *args, **kwargs):
        # Normalize only the `normalized_field` before saving
        self.sense = strip_and_normalize('NFC', self.sense)
        #process language
        self.language = self.language.strip().lower()

        is_new = self._state.adding
        user = kwargs.pop('user', None)  
        # Handle the user for created_by and modified_by
        if is_new and user:
            self.created_by = user
        elif not is_new:
            self.modified_at = timezone.now()
            self.modified_by = user

            # Ensure 'modified_at' and 'modified_by' are included in 'update_fields'
            if 'update_fields' in kwargs:
                update_fields = set(kwargs['update_fields'])
                update_fields.update({'modified_at', 'modified_by'})
                kwargs['update_fields'] = list(update_fields)

        super().save(*args, **kwargs)
