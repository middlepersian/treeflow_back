from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import \
    Corpus, Text,\
    Feature, Dependency,\
    Token, BibEntry, Comment, Section, SectionToken

class TokenHistoryAdmin(SimpleHistoryAdmin):
    list_display = ["transcription", "transliteration",  "previous"]
    search_fields = ['transcription']

class TextAdmin(admin.ModelAdmin):
    list_display = ('title', 'identifier', 'stage', 'created_at')


admin.site.register(BibEntry)
admin.site.register(Corpus)
admin.site.register(Text, TextAdmin)

admin.site.register(Token, TokenHistoryAdmin)
admin.site.register(Feature)
admin.site.register(Dependency)
admin.site.register(Comment)
admin.site.register(Section)
admin.site.register(SectionToken)