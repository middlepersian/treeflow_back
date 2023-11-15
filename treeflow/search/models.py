from django.db import models


class SearchForm(models.Model):
    search_input = models.CharField(max_length=255)
    criteria_value = models.IntegerField(default=0)
    criteria_scope = models.CharField(max_length=255)
    lemmas_word = models.CharField(max_length=255)
    toggle_field = models.BooleanField(default=False)
