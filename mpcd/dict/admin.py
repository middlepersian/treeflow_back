from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from django.db.models.functions import Lower
from .models import Dictionary, Entry, Lemma, LoanWord, Translation, Category, Reference, Definition


class EntryHistoryAdmin(SimpleHistoryAdmin):
    fields = ["dict", "lemma", "loanwords",  "translations", "definitions", "categories", "references", "comment"]
    list_display = ["lemma", "_loanwords",  "_translations", "_definitions", "_categories", "_references", "comment"]
    history_list_display = ["lemma"]
    search_fields = ["lemma__word", "translations__meaning"]

    def get_ordering(self, request):
        return ['lemma__word']

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
                trans = " - \n".join([t.meaning for t in p.translations.all()])
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


class WordHistoryAdmin(SimpleHistoryAdmin):
    fields = ["word", "language"]
    list_display = ["word", "language"]
    history_list_display = ["word", "language"]
    search_fields = ["word"]

    def get_ordering(self, request):
        return ['word']


class LoanWordHistoryAdmin(SimpleHistoryAdmin):
    fields = ["language", "word", "translations"]
    list_display = [ "word", "_translations", "language",]
    history_list_display = ["language", "word", ]
    search_fields = ["word", "translations__meaning"]

    def get_ordering(self, request):
        return ['word']

    def get_queryset(self, request):
        queryset = LoanWord.objects.all()
        queryset = queryset.prefetch_related('translations')
        return queryset

    def _translations(self, obj):
        return " |\n".join([p.meaning for p in obj.translations.all()])


class TranslationHistoryAdmin(SimpleHistoryAdmin):
    fields = ["meaning", "language"]
    list_display = ["meaning", "language"]
    history_list_display = ["meaning", "language"]
    search_fields = ["meaning"]

    def get_ordering(self, request):
        return ['meaning']


class DefinitionHistoryAdmin(SimpleHistoryAdmin):
    fields = ["definition", "language"]
    list_display = ["definition", "language"]
    history_list_display = ["definition", "language"]
    search_fields = ["definition"]

    def get_ordering(self, request):
        return ['definition']


class ReferenceHistoryAdmin(SimpleHistoryAdmin):
    fields = ["reference"]
    list_display = ["reference"]
    history_list_display = ["reference"]
    search_fields = ["reference"]

    def get_ordering(self, request):
        return ["reference"]


admin.site.register(Dictionary)
admin.site.register(Entry, EntryHistoryAdmin)
admin.site.register(Lemma, WordHistoryAdmin)
admin.site.register(LoanWord, LoanWordHistoryAdmin)
admin.site.register(Translation, TranslationHistoryAdmin)
admin.site.register(Definition, DefinitionHistoryAdmin)
admin.site.register(Category)
admin.site.register(Reference, ReferenceHistoryAdmin)
