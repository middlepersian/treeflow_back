from typing import TYPE_CHECKING
from django.db import models
from simple_history.models import HistoricalRecords
from .source import Source


if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager


class Codex(Source):
    codex_part_codex: "RelatedManager[CodexPart]"

    # TODO add :

    #id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)

    sigle = models.CharField(max_length=5, unique=True)
    comments = models.ManyToManyField('Comment', blank=True, related_name='codex_comments')

    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.sigle)
