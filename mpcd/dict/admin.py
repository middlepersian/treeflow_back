from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Dictionary, Entry, Word, LoanWord, Translation, Category, Reference, Definition



class EntryHistoryAdmin(SimpleHistoryAdmin):
    list_display = [ "lemma",]
    history_list_display = ["lemma"]
    search_fields = ["lemma",]

admin.site.register(Dictionary)
admin.site.register(Entry, EntryHistoryAdmin)
admin.site.register(LoanWord)
admin.site.register(Word)
admin.site.register(Translation)
admin.site.register(Category)
admin.site.register(Reference)
admin.site.register(Definition)


