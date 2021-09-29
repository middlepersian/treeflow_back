import uuid as uuid_lib
from django.db import models
from django.db.models.fields import CharField, URLField
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
    leg = 'legal', 'legal'
    eco = 'econ', 'economy'
    the = 'theo', 'theology'
    rit = 'ritual', 'ritual'
    geo = 'geo', 'geography'
    myt = 'myth', 'mythology'



class Dictionary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=10)
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
    language = models.ForeignKey(Lang, on_delete=models.CASCADE, null=True)
    meaning = models.CharField(unique=True, max_length=50)

    history = HistoricalRecords()

    def __str__(self):
        return self.meaning


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    category = models.CharField(max_length=6, choices=CatCh.choices, unique=True)

    def __str__(self):
        return '{}'.format(self.category)


class Reference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    reference = models.CharField(unique=True, max_length=50, null=True, blank=True)
    url = URLField(null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.reference)


class Word(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    word = models.CharField(unique=True, max_length=50)
    language = models.ForeignKey(Lang, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '{} {}'.format(self.language, self.word)


class LoanWord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    word = models.CharField(unique=True, max_length=50)
    language = models.ForeignKey(Lang, on_delete=models.CASCADE, null=True)
    translation = models.ManyToManyField(Translation)

    def __str__(self):
        return '{} {}'.format(self.language, self.word)


class Definition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    definition = CharField(unique=True, max_length=350, null=True, blank=True)
    language = models.ForeignKey(Lang, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '{} {}'.format(self.language, self.definition)


class Entry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    dict = models.ForeignKey(Dictionary, on_delete=models.CASCADE, blank=True)
    lemma = models.OneToOneField(Word, on_delete=models.CASCADE, related_name='entry_lemma')
    loanword = models.ForeignKey(LoanWord, on_delete=models.CASCADE, blank=True, null=True)
    translation = models.ManyToManyField(Translation, blank=True)
    definition = models.ManyToManyField(Definition, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    literature = models.ManyToManyField(Reference, blank=True)
    comment = models.TextField(max_length=300, null=True, blank=True)
    cross_reference = models.ManyToManyField(Word, related_name='entry_cross_reference', blank=True)
    history = HistoricalRecords()

    def _translation(self):
        return "|\n".join([p.meaning for p in self.translation.all()])

    def __str__(self):
        return '{}'.format(self.lemma)
