from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import \
    Corpus, Text,\
    Feature, Dependency,\
    Token, BibEntry, Comment, Section, SectionToken, POS, Source

class TokenHistoryAdmin(SimpleHistoryAdmin):
    list_display = ["transcription", "transliteration",  "previous"]
    search_fields = ['transcription']

class TextAdmin(admin.ModelAdmin):
    list_display = ('title', 'identifier', 'stage', 'created_at')

# SectionAdmin
# this Admin class should filter for sections with tokens, that have dependencies
class SectionAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'type','text' , 'title', 'language', 'created_at','has_Enhanced')
    list_filter = ('type', 'text',)
    search_fields = ['title']
    
class SourceAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'type')
    list_filter = ('type',)
    search_fields = ['identifier']
    

#DependencyAdmin
class DependencyAdmin(admin.ModelAdmin):
    list_display = ('token', 'head', 'rel', 'created_at','enhanced')
    list_filter = ('enhanced', 'rel')


admin.site.register(BibEntry)
admin.site.register(Corpus)
admin.site.register(Text, TextAdmin)

admin.site.register(Token, TokenHistoryAdmin)
admin.site.register(Feature)
admin.site.register(Dependency,DependencyAdmin)
admin.site.register(Comment)
admin.site.register(Section, SectionAdmin)
admin.site.register(SectionToken)
admin.site.register(POS)
admin.site.register(Source, SourceAdmin)