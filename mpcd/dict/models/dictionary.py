import uuid as uuid_lib
from django.contrib.postgres.fields import IntegerRangeField
from django.db import models
from django.db.models.fields import CharField, URLField
from django.urls import reverse
from simple_history.models import HistoricalRecords


class Dictionary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=10)
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class LangCh(models.TextChoices):
    # iso 639-3
    akk = 'akk', 'Akkadian'
    arc = 'arc', 'Imperial Aramaic (700-300 BCE), Official Aramaic (700-300 BCE)'
    ave = 'ave', 'Avestan'
    eng = 'eng', 'English'
    deu = 'deu', 'German'
    grc = 'grc', 'Ancient Greek (to 1453)'
    pal = 'pal', 'Pahlavi'
    xpr = 'xpr', 'Parthian'


class CatCh(models.TextChoices):
    leg = 'leg', 'legal'
    eco = 'eco', 'economy'
    the = 'the', 'theology'
    rit = 'rit', 'ritual'
    geo = 'geo', 'geography'
    myt = 'myt', 'mythology'


class Lang(models.Model):
    language = models.CharField(max_length=3, choices=LangCh.choices, unique=True)

    def __str__(self):
        return '{}'.format(self.language)


class LoanWord(models. Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    word = models.CharField(unique=True, max_length=30, null=True)
    language = models.ForeignKey(Lang, on_delete=models.CASCADE, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return '{} - {}'.format(self.language, self.word)


class Translation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    language = models.ForeignKey(Lang, on_delete=models.CASCADE, null=True)
    meaning = models.CharField(unique=True, max_length=50)

    history = HistoricalRecords()

    def __str__(self):
        return self.meaning


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    category = models.CharField(max_length=5, choices=CatCh.choices, unique=True)

    def __str__(self):
        return '{}'.format(self.category)


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    name = models.CharField(max_length=20, null=True, blank=True)
    lastname = models.CharField(max_length=20, null=True, blank=True)
    # TODO create constrain name + lastname

    def __str__(self):
        return '{} {}'.format(self.name, self.lastname)


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    title = models.CharField(max_length=100, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True)
    year = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.title, self.author, self.year)


class Reference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True)
    pages = IntegerRangeField(null=True, blank=True)
    url = URLField(null=True, blank=True)

    def __str__(self):
        return '{} {}'.format(self.book, self.pages)


class Lemma(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    lemma = models.CharField(unique=True, max_length=50)
    language = models.ForeignKey(Lang, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '{} {}'.format(self.language, self.lemma)


class Definition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    definition = CharField(unique=True, max_length=350, null=True, blank=True)
    language = models.ForeignKey(Lang, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '{} {}'.format(self.language, self.definition)


class Entry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    dict = models.ForeignKey(Dictionary, on_delete=models.CASCADE, blank=True)
    lemma = models.OneToOneField(Lemma, on_delete=models.CASCADE, related_name='entry_lemma')
    loanword = models.ManyToManyField(LoanWord, blank=True)
    translation = models.ManyToManyField(Translation, blank=True)
    definition = models.ManyToManyField(Definition, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    literature = models.ManyToManyField(Reference, blank=True)
    comment = models.TextField(max_length=300, null=True, blank=True)
    cross_reference = models.ManyToManyField(Lemma, related_name='entry_cross_reference', blank=True)
    history = HistoricalRecords()

    def _translation(self):
        return "|\n".join([p.meaning for p in self.translation.all()])

    def __str__(self):
        return '{}'.format(self.lemma)
