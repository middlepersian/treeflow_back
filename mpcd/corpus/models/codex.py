from django.db import models
from simple_history.models import HistoricalRecords
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
    sigle = models.CharField(max_length=10, unique=True, choices=CodexCh.choices, default="")

    history = HistoricalRecords()

    def __str__(self):
        return '{} {}'.format(self.sigle, self.title)
