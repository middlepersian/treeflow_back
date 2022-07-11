import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from django.conf import settings
from .comment_category import CommentCategory


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    categories = models.ManyToManyField(CommentCategory, blank=True, related_name='comment_category')
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return '{} {} {}'.format(self.user, self.category, self.text)
