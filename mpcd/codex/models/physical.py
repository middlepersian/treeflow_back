import uuid as uuid_lib

from django.db import models
from django.urls import reverse


class Codex(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return '{}'.format(self.name)


class Folio(models.Model):
    codex_id = models.ForeignKey(Codex, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)    
    def __str__(self):
        return '{}'.format(self.name)


class Side(models.Model):
    folio_id = models.ForeignKey(Folio, on_delete=models.CASCADE)
    name = models.CharField(max_length=100) 
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return '{}'.format(self.name)


class Line(models.Model):
    side_id = models.ForeignKey(Side, on_delete=models.CASCADE)
    number = models.IntegerField()
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)   

    def __str__(self):
        return '{}'.format(self.number)
