from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from django.db.models.functions import Lower
from .models import Dictionary, Entry, Word, LoanWord, Translation, Category, Reference, Definition



class EntryHistoryAdmin(SimpleHistoryAdmin):
    fields = ["lemma", "loanwords",  "translations", "definitions", "categories", "references", "comment"]
    list_display = [ "lemma", "_loanwords",  "_translations", "_definitions", "_categories", "_references", "comment"]
    history_list_display = ["lemma"]
    search_fields = ["lemma__word",]

    def get_ordering(self, request):
        return ['lemma__word']  # sort case insensitive

    def get_queryset(self, request):

        queryset = Entry.objects.all()
        queryset = queryset.select_related('dict')
        queryset = queryset.select_related('lemma')
        queryset = queryset.prefetch_related('loanwords', 'loanwords__translations')
        queryset = queryset.prefetch_related('translations')
        queryset = queryset.prefetch_related('definitions')
        queryset = queryset.prefetch_related('categories')
        queryset = queryset.prefetch_related('references')
        return queryset


    def _loanwords(self, obj):
        loans = []
        for p in obj.loanwords.all():
            if p.language:
                lang = p.language
                loans.append(lang)
            if p.word:
                loanword = p.word
                loans.append(loanword)
            if p.translations:
                trans = " - \n".join([t.meaning for t in obj.translations.all()])
                loans.append(trans)

        return " |\n".join([p for p in loans])

    def _translations(self, obj):
        return " |\n".join([p.meaning for p in obj.translations.all()])

    def _definitions(self, obj):
        return " |\n".join([p.definition for p in obj.definitions.all()])    

    def _categories(self, obj):
        return " |\n".join([p.category for p in obj.categories.all()])       

    def _references(self, obj):
        return " |\n".join([p.reference for p in obj.references.all()])    
    

admin.site.register(Dictionary)
admin.site.register(Entry, EntryHistoryAdmin)
admin.site.register(LoanWord)
admin.site.register(Word)
admin.site.register(Translation)
admin.site.register(Category)
admin.site.register(Reference)
admin.site.register(Definition)


