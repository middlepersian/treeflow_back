#from mpcd.dict.models import Meaning
from .text import Text
from .token import Token
from .comment import Comment
from django.db import models
import uuid as uuid_lib
from simple_history.models import HistoricalRecords
from django.contrib.auth import get_user_model

User = get_user_model()


class Sentence(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    text = models.ForeignKey(Text, on_delete=models.CASCADE, null=True, blank=True, related_name='sentence_text')
    tokens = models.ManyToManyField(Token, related_name='sentence_tokens')

    translations = models.ManyToManyField('dict.Meaning', related_name='sentence_translations')
    comments = models.ManyToManyField(Comment, blank=True, related_name = 'sentence_comments')

    number = models.FloatField(null=True, blank=True)
    previous = models.OneToOneField('self',
                                    related_name='next',
                                    blank=True,
                                    null=True,
                                    on_delete=models.SET_NULL)

    history = HistoricalRecords()

    class Meta:
        ordering = ['number']
        constraints = [
            models.UniqueConstraint(
                fields=['number', 'text'], name='sentence_number_text'
            )
        ]

    def get_tokens(self):
        return " | ".join([p.transcription for p in self.tokens.all()])

    def __str__(self):
        return '{} - {} - {}'.format(self.text, self.number, self.get_tokens())
    
