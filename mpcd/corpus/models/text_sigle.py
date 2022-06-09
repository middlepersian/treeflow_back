import uuid as uuid_lib
from django.db import models


class TextSigle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    sigle = models.CharField(max_length=10)
    genre = models.CharField(max_length=3)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['sigle', 'genre'], name='sigle_genre'
            )
        ]

    def __str__(self):
        return '{} , {}'.format(self.sigle, self.genre)
