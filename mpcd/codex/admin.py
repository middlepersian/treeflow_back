from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Codex, Folio, Side, Line, Text, Chapter, Section, Sentence, Strophe, Verse, MorphologicalAnnotation, Dependency, SyntacticAnnotation, Token, CodexToken, Feature, FeatureValue, Pos



class TokenHistoryAdmin(SimpleHistoryAdmin):
    list_display = [ "transcription", "transliteration","lemma", "pos" ,"ms_features", "syntax_annotations"]
    history_list_display = [ "pos" ]
    search_fields = ['transcription', 'comment']
class CodexTokenHistoryAdmin(TokenHistoryAdmin): 
    list_display = [ "transcription", "transliteration","lemma", "pos" ,"ms_features", "syntax_annotations" , "line_id", "position"]




admin.site.register(Codex)
admin.site.register(Folio)
admin.site.register(Side)
admin.site.register(Line)
admin.site.register(Text)
admin.site.register(Chapter)
admin.site.register(Section)
admin.site.register(Sentence)
admin.site.register(Strophe)
admin.site.register(Verse)
admin.site.register(MorphologicalAnnotation)
admin.site.register(Feature)
admin.site.register(FeatureValue)
admin.site.register(Pos)
admin.site.register(Dependency)
admin.site.register(SyntacticAnnotation)
admin.site.register(Token, TokenHistoryAdmin)
admin.site.register(CodexToken, CodexTokenHistoryAdmin)
