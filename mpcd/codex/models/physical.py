import uuid as uuid_lib

from django.db import models
from django.urls import reverse
from simple_history.models import HistoricalRecords
from .token import Token

class Codex(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=255, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.name)


class Folio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    name = models.CharField(max_length=100)
    codex = models.ForeignKey(Codex, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.name)



class Side(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    name = models.CharField(max_length=100)
    folio = models.ForeignKey(Folio, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return '{} {}'.format(self.folio, self.name)

class Line(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    number = models.IntegerField()
    side = models.ForeignKey(Side, on_delete=models.DO_NOTHING)
    comment = models.TextField(blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return '{} {}'.format(self.side, self.number)


## TODO: write constrain for position
class CodexToken(Token):
    line = models.ForeignKey(Line, on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField(null=True)
    history = HistoricalRecords()
    def __str__(self):
        return self.transcription
