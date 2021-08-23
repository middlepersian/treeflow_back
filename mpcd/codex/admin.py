from django.contrib import admin

from .models import Codex, Folio, Side, Line, Text, Chapter, Section, Strophe, Verse, TokenSemantics, MorphologicalAnnotation, Dependency, SyntacticAnnotation, Token, CodexToken

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
admin.site.register(Dependency)
admin.site.register(SyntacticAnnotation)
admin.site.register(Token)
admin.site.register(CodexToken)
