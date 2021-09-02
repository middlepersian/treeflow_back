import uuid as uuid_lib

from django.db import models
from django.urls import reverse
from simple_history.models import HistoricalRecords
from .token import Token

class Codex(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    description = models.TextField(blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.name)


class Folio(models.Model):
    codex_id = models.ForeignKey(Codex, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    description = models.TextField(blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.name)



class Side(models.Model):
    folio_id = models.ForeignKey(Folio, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    description = models.TextField(blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return '{} {}'.format(self.folio_id, self.name)

class Line(models.Model):
    side_id = models.ForeignKey(Side, on_delete=models.DO_NOTHING)
    number = models.IntegerField()
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    description = models.TextField(blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return '{} {}'.format(self.side_id, self.number)


## TODO: write constrain for position
class CodexToken(Token):
    line_id = models.ForeignKey(Line, on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField(null=True)
    history = HistoricalRecords()
    def __str__(self):
        return self.transcription
