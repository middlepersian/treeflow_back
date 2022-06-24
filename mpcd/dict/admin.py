from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Dictionary, Lemma, Reference, Meaning



class WordHistoryAdmin(SimpleHistoryAdmin):
    fields = ["word", "language"]
    list_display = ["word", "language"]
    history_list_display = ["word", "language"]
    search_fields = ["word"]

    def get_ordering(self, request):
        return ['word']


class ReferenceHistoryAdmin(SimpleHistoryAdmin):
    fields = ["reference"]
    list_display = ["reference"]
    history_list_display = ["reference"]
    search_fields = ["reference"]

    def get_ordering(self, request):
        return ["reference"]


admin.site.register(Dictionary)
admin.site.register(Lemma, WordHistoryAdmin)
admin.site.register(Reference, ReferenceHistoryAdmin)
admin.site.register(Meaning)
