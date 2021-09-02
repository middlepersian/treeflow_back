from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Codex, Folio, Side, Line, Text, Chapter, Section, Strophe, Verse, TokenSemantics, MorphologicalAnnotation, Dependency, SyntacticAnnotation, Token, CodexToken, Feature, FeatureValue



class TokenHistoryAdmin(SimpleHistoryAdmin):
    list_display = [ "token", ]
    history_list_display = ["transliteration"]
    search_fields = ['token', 'comment']


admin.site.register(Codex)
admin.site.register(Folio)
admin.site.register(Side)
admin.site.register(Line)
admin.site.register(Text)
admin.site.register(Chapter)
admin.site.register(Section)
admin.site.register(Strophe)
admin.site.register(Verse)
admin.site.register(TokenSemantics)
admin.site.register(MorphologicalAnnotation)
admin.site.register(Feature)
admin.site.register(FeatureValue)
admin.site.register(Dependency)
admin.site.register(SyntacticAnnotation)
admin.site.register(Token, TokenHistoryAdmin)
admin.site.register(CodexToken)
