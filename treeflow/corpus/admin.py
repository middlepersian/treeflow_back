from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import \
    Corpus, Text,\
    Feature, Dependency,\
    Token, BibEntry, Comment

class TokenHistoryAdmin(SimpleHistoryAdmin):
    list_display = ["transcription", "transliteration",  "previous"]
    search_fields = ['transcription']


admin.site.register(BibEntry)
admin.site.register(Corpus)
admin.site.register(Text)

admin.site.register(Token, TokenHistoryAdmin)
admin.site.register(Feature)
admin.site.register(Dependency)
admin.site.register(Comment)