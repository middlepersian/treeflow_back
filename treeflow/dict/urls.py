from django.urls import include, path
from treeflow.dict.views.save_sense import save_sense
from treeflow.dict.views.save_lemma import save_lemma
from django.views.generic import TemplateView
from treeflow.dict.views.lemma_details import lemma_details

from treeflow.dict.views.lemmas_list import lemmas_list
from treeflow.dict.views.lemma_edit import lemma_edit
from treeflow.dict.views.update_lemma import update_lemma
from treeflow.dict.views.filter_lemmas import filter_lemmas
from treeflow.dict.views.fetch_alphabet import fetch_alphabet
from treeflow.dict.views.dictionary_entry import lemma_details

app_name = "treeflow.dict"
urlpatterns = [
        path("save_sense/", save_sense, name="save_sense"),
        path("save_lemma/", save_lemma, name="save_lemma"),
        path("", lemmas_list, name="dictionary"),
        path("<uuid:lemma_id>/", lemmas_list, name="lemmas"),
        path("fetch_Lemma/<uuid:lemma_id>/",lemma_details, name="lemma_details"),
        path("edit_Lemma/<uuid:lemma_id>/", lemma_edit, name="lemma_edit"),
        path("update_lemma/<uuid:lemma_id>/", update_lemma, name="update_lemma"),
        path("filter_lemmas/", filter_lemmas, name="filter_lemmas"),
        path("fetch_alphabet/", fetch_alphabet, name="fetch_alphabet"),
        path("fetch_attestations/<uuid:lemma_id>/",lemma_details, name="fetch_attestations")
]