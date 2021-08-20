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


class Folio(models.Model):
    codex_id = models.ForeignKey(Codex, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)    


class Side(models.Model):
    folio_id = models.ForeignKey(Folio, on_delete=models.CASCADE)
    name = models.CharField(max_length=255) 
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)


class Line(models.Model):
    side_id = models.ForeignKey(Side, on_delete=models.CASCADE)
    number = models.IntegerField()
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)    