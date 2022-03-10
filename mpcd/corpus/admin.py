from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Codex, Folio, Line, Edition, TextSigle, \
    Corpus, Resource, Text, Sentence,\
    MorphologicalAnnotation, Dependency,\
    Token, Source, Author, BibEntry
4

class TokenHistoryAdmin(SimpleHistoryAdmin):
    raw_id_fields = ['lemma']
    list_display = ["transcription", "transliteration", "pos","comment", "previous"]
    history_list_display = ["pos"]
    search_fields = ['transcription', 'comment']


class BibEntryHistoryAdmin(SimpleHistoryAdmin):
    list_display = ["get_authors", "title", "year"]


admin.site.register(Author)
admin.site.register(BibEntry, BibEntryHistoryAdmin)

admin.site.register(Codex)
admin.site.register(Folio)
admin.site.register(Line)
admin.site.register(Resource)
admin.site.register(Edition)
admin.site.register(TextSigle)

admin.site.register(Source)

admin.site.register(Corpus)
admin.site.register(Text)
admin.site.register(Sentence)

admin.site.register(Token, TokenHistoryAdmin)
admin.site.register(MorphologicalAnnotation)
admin.site.register(Dependency)
