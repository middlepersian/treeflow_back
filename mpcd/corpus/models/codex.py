from mpcd.corpus.models.author import Author
import uuid as uuid_lib

from django.db import models
from simple_history.models import HistoricalRecords
from .token import Token
from .bibliography import BibEntry
from .source import Source


class CodexCh(models.TextChoices):
    mk = 'MK', 'MK'
    td1 = 'TD1', 'TD1'
    td4a = 'TD4a', 'TD4a'
    dh6 = 'DH6', 'DH6'
    bk = 'BK', 'BK'
    td2 = 'TD2', 'TD2'
    mj = 'MJ', 'Minocher Jamaspji62(Dd)'
    iol = 'IOL', 'IOL CCXXVIII (PRDd)'
    b = 'B', 'B'
    p = 'P', 'P'
    m51 = 'M51', 'M51'
    k20 = 'K20', 'K20'
    k20b = 'K20b', 'K20b'
    k27 = 'K27', 'K27'
    k35 = 'K35', 'K35'
    k43a = 'K43a', 'K43a'
    k43b = 'K43b', 'K43b'
    k26 = 'K26', 'K26'
    msmdh = 'msMHD', 'MS of MHD'


class Codex(Source):
    #id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    #name = models.CharField(max_length=255)
    #slug = models.SlugField(unique=True)
    #description = models.CharField(max_length=255, blank=True)
    sigle = models.CharField(max_length=10, unique=True, choices=CodexCh.choices, default="")
    scribe = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True, null=True)
    library = models.CharField(max_length=100,  blank=True)
    signature = models.CharField(max_length=100,  blank=True)
    facsimile = models.ManyToManyField(BibEntry,  blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return '{} {}'.format(self.slug, self.sigle)


class Folio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    name = models.CharField(max_length=100)
    codex = models.ForeignKey(Codex, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.name)


class Line(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    number = models.IntegerField()
    side = models.ForeignKey(Folio, on_delete=models.DO_NOTHING)
    comment = models.TextField(blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return '{} {}'.format(self.side, self.number)


# TODO: write constrain for position
class CodexToken(Token):
    line = models.ForeignKey(Line, on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField(null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.transcription
