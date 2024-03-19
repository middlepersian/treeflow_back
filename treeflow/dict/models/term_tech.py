import uuid as uuid_lib
from django.db import models


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


class TermTech(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    category = models.CharField(max_length=10, choices=CatCh.choices, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return '{}'.format(self.category)
