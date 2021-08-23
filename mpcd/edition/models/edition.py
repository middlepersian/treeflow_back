import uuid as uuid_lib

from django.db import models
from django.urls import reverse

from mpcd.codex.models.token import Token

class Edition(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)

class Text(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    edition_id = models.ForeignKey(Edition, on_delete=models.CASCADE)


class Chapter (models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    text_id = models.ForeignKey(Text, on_delete=models.CASCADE)

class Section (models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    chapter_id = models.ForeignKey(Chapter, on_delete=models.CASCADE)

class Sentence (models. Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    section_id = models.ForeignKey(Section, on_delete=models.CASCADE)
    tokens =  models.ForeignKey(Token, on_delete=models.CASCADE, related_name='edition_tokens')    