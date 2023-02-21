from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Dictionary, Lemma, Meaning




admin.site.register(Dictionary)
admin.site.register(Lemma)
admin.site.register(Meaning)
## TODO Semantic
