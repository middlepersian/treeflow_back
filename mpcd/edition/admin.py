from django.contrib import admin
from .models import Edition, Text, Chapter, Section, Sentence

admin.site.register(Edition)
admin.site.register(Text)
admin.site.register(Chapter)
admin.site.register(Section)
admin.site.register(Sentence)
