from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from django.db.models.functions import Lower
from .models import Dictionary, Entry, Word, LoanWord, Translation, Category, Reference, Definition



class EntryHistoryAdmin(SimpleHistoryAdmin):
    list_display = [ "lemma", "_loanwords",  "_translations", "_definitions", "_categories", "_references", "comment"]
    history_list_display = ["lemma"]
    search_fields = ["lemma__word",]
    def get_ordering(self, request):
        return ['lemma__word']  # sort case insensitive

admin.site.register(Dictionary)
admin.site.register(Entry, EntryHistoryAdmin)
admin.site.register(LoanWord)
admin.site.register(Word)
admin.site.register(Translation)
admin.site.register(Category)
admin.site.register(Reference)
admin.site.register(Definition)


