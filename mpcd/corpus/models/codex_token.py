from django.db import models
from .token import Token
from .line import Line
from simple_history.models import HistoricalRecords


# TODO: write constrain for position
class CodexToken(Token):
    line = models.ForeignKey(Line, on_delete=models.SET_NULL, null=True, related_name='codex_token_line')
    position = models.PositiveSmallIntegerField(null=True)
    history = HistoricalRecords(inherit=True)

    def __str__(self):
        return self.transcription
