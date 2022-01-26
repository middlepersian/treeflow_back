import uuid as uuid_lib
from django.db import models


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'last_name'], name='name_lastname'
            )
        ]

    def __str__(self):
        return '{}, {}'.format(self.last_name, self.name)
