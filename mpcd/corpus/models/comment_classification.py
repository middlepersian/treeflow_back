import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from django.conf import settings
from .comment_category import CommentCategory


class CommentClassification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    #tag = uncertain|to_discuss|new_suggestion
    tag  = models.CharField(max_length=20, null=True, blank=True)
    # catergories: "C"|"L"|"S"|"M"|"X"
    categories = models.ManyToManyField(CommentCategory, blank=True, related_name='comment_categories')
    history = HistoricalRecords()
