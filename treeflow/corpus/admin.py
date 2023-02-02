from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Codex,  Facsimile, Folio, Edition, TextSigle, \
    Corpus, Resource, Text,\
    MorphologicalAnnotation, Dependency,\
    Token, Source, Author, BibEntry, Comment

class TokenHistoryAdmin(SimpleHistoryAdmin):
    list_display = ["transcription", "transliteration", "pos", "previous"]
    history_list_display = ["pos"]
    search_fields = ['transcription']


admin.site.register(Author)
admin.site.register(BibEntry)

admin.site.register(Codex)
admin.site.register(Facsimile)

admin.site.register(Folio)
admin.site.register(Resource)
admin.site.register(Edition)
admin.site.register(TextSigle)

admin.site.register(Source)

admin.site.register(Corpus)
admin.site.register(Text)

admin.site.register(Token, TokenHistoryAdmin)
admin.site.register(MorphologicalAnnotation)
admin.site.register(Dependency)
admin.site.register(Comment)