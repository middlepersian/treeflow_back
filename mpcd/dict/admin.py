from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Dictionary, Entry, Lemma, Lang, LoanWord, Translation, Category, Author, Book, Reference, Definition



class EntryHistoryAdmin(SimpleHistoryAdmin):
    list_display = [ "lemma", "_translation"]
    history_list_display = ["lemma"]
    search_fields = ["lemma", "_translation"]

admin.site.register(Dictionary)
admin.site.register(Entry, EntryHistoryAdmin)
admin.site.register(Lemma)
admin.site.register(Lang)
admin.site.register(LoanWord)
admin.site.register(Translation)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Reference)
admin.site.register(Definition)


