
from .text import Text
from .token import Token
from django.db import models
import uuid as uuid_lib
from simple_history.models import HistoricalRecords
from django.contrib.auth import get_user_model
User = get_user_model()


class Sentence(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    text = models.ForeignKey(Text, on_delete=models.CASCADE, null=True, blank=True, related_name='sentence_text')
    tokens = models.ManyToManyField(Token, related_name='sentence_tokens')

    translation = models.TextField(null=True, blank=True)
    comment = models.CharField(max_length=255, blank=True)

    history = HistoricalRecords(inherit=True)

    def get_tokens(self):
        return "|".join([p.transcription for p in self.tokens.all()])
