import uuid as uuid_lib

from django.db import models
from django.urls import reverse
from simple_history.models import HistoricalRecords


class Codex(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    history = HistoricalRecords()
    description = models.TextField(blank=True)

    def __str__(self):
        return '{}'.format(self.name)


class Folio(models.Model):
    codex_id = models.ForeignKey(Codex, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    description = models.TextField(blank=True)    
<<<<<<< HEAD
    def __str__(self):
        return '{}'.format(self.name)
=======
    history = HistoricalRecords()
>>>>>>> 91e78ada7efe5e81fabfc78237cc26f6e353adb0


class Side(models.Model):
    folio_id = models.ForeignKey(Folio, on_delete=models.CASCADE)
    name = models.CharField(max_length=100) 
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    description = models.TextField(blank=True)
<<<<<<< HEAD
    def __str__(self):
        return '{}'.format(self.name)
=======
    history = HistoricalRecords()
>>>>>>> 91e78ada7efe5e81fabfc78237cc26f6e353adb0


class Line(models.Model):
    side_id = models.ForeignKey(Side, on_delete=models.CASCADE)
    number = models.IntegerField()
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
<<<<<<< HEAD
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)   

    def __str__(self):
        return '{}'.format(self.number)
=======
    description = models.TextField(blank=True)    
    history = HistoricalRecords()
>>>>>>> 91e78ada7efe5e81fabfc78237cc26f6e353adb0
