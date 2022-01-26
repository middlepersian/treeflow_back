import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords


class CatCh(models.TextChoices):
    astr = "astr",  "astronomy"
    bot = "bot",  "botany"
    econom = "econom",  "economy"
    geo = "geogr",  "geography"
    legal = "legal",  "legal"
    measure = "measure",  "measurement"
    med = "med",  "medicine"
    myth = 'myth', 'mythology'
    philos = "philos",  "philosophy"
    pol = "pol",  "politics"
    purity = "purity",  "purity"
    ritual = "ritual",  "ritual"
    theol = "theol",  "theology"
    zool = "zool",  "zoology"


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    category = models.CharField(max_length=10, choices=CatCh.choices, unique=True)

    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.category)
