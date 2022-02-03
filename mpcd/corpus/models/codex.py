from django.db import models
from simple_history.models import HistoricalRecords
from .source import Source
from .author import Author
from .bibliography import BibEntry


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
    sigle = models.CharField(max_length=10, unique=True, choices=CodexCh.choices, default="")
    copy_date = models.TextField(null=True, blank=True)

    copy_place_name = models.CharField(max_length=100, null=True, blank=True)
    copy_place_latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    copy_place_longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    library = models.CharField(max_length=100,  blank=True)
    signature = models.CharField(max_length=100,  blank=True)
    scribes = models.ManyToManyField(Author, blank=True, related_name='codex_scribes')
    facsimiles = models.ManyToManyField(BibEntry,
                                        blank=True, related_name='codex_facsimiles')

    history = HistoricalRecords()

    def __str__(self):
        return '{} {}'.format(self.sigle, self.title)
