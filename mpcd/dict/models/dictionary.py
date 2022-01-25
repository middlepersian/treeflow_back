import uuid as uuid_lib
from django.db import models
from django.db.models.fields import TextField, URLField
from simple_history.models import HistoricalRecords


class LangCh(models.TextChoices):
    # iso 639-3
    akk = 'akk', 'Akkadian'
    arc = 'arc', 'Imperial Aramaic (700-300 BCE), Official Aramaic (700-300 BCE)'
    ave = 'ave', 'Avestan'
    eng = 'eng', 'English'
    deu = 'deu', 'German'
    fra = 'fra', 'French'
    grc = 'grc', 'Ancient Greek (to 1453)'
    ita = 'ita', 'Italian'
    pal = 'pal', 'Pahlavi'
    spa = 'spa', 'Spanish'
    xpr = 'xpr', 'Parthian'


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


class Dictionary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=10, unique=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Lang(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    language = models.CharField(max_length=3, choices=LangCh.choices, unique=True)

    def __str__(self):
        return '{}'.format(self.language)


class Translation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    language = models.CharField(max_length=3, choices=LangCh.choices, blank=True, null=True)
    meaning = models.TextField(unique=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.meaning


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    category = models.CharField(max_length=10, choices=CatCh.choices, unique=True)

    def __str__(self):
        return '{}'.format(self.category)


class Reference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    reference = models.CharField(unique=True, max_length=350, null=True, blank=True)
    url = URLField(null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.reference)


class Word(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    word = models.CharField(unique=True, max_length=100)
    language = models.CharField(max_length=3, choices=LangCh.choices, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.word)


class LoanWord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    word = models.CharField(unique=True, max_length=50)
    language = models.CharField(max_length=3, choices=LangCh.choices, blank=True, null=True)
    translations = models.ManyToManyField(Translation, blank=True)

    def __str__(self):
        return '{} {}'.format(self.language, self.word)


class Definition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    definition = TextField(unique=True, null=True, blank=True)
    language = models.CharField(max_length=3, choices=LangCh.choices, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.definition)


class Entry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    dict = models.ForeignKey(Dictionary, on_delete=models.CASCADE, blank=True)
    lemma = models.OneToOneField(Word, on_delete=models.CASCADE, related_name="lemma_entry")
    loanwords = models.ManyToManyField(LoanWord, blank=True)
    translations = models.ManyToManyField(Translation, blank=True)
    definitions = models.ManyToManyField(Definition, blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    references = models.ManyToManyField(Reference, blank=True)
    comment = models.TextField(null=True, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.lemma)
