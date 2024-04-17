from django.urls import include, path
from treeflow.dict.views.save_sense import save_sense
from treeflow.dict.views.save_lemma import save_lemma
from django.views.generic import TemplateView
from treeflow.dict.views.lemma_details import lemma_details

from treeflow.dict.views.lemmas_list import lemmas_list
from treeflow.dict.views.lemma_edit import lemma_edit
from treeflow.dict.views.update_lemma import update_lemma
from treeflow.dict.views.filter_lemmas import filter_lemmas

app_name = "treeflow.dict"
urlpatterns = [
        path("save_sense/", save_sense, name="save_sense"),
        path("save_lemma/", save_lemma, name="save_lemma"),
        path("dictionary/", lemmas_list, name="dictionary"),
        path("dictionary/<uuid:lemma_id>/", lemmas_list, name="lemmas"),
        path("dictionary/fetch_Lemma/<uuid:lemma_id>/",lemma_details, name="lemma_details"),
        path("dictionary/edit_Lemma/<uuid:lemma_id>/", lemma_edit, name="lemma_edit"),
        path("dictionary/update_lemma/<uuid:lemma_id>/", update_lemma, name="update_lemma"),
        path("dictionary/filter_lemmas/", filter_lemmas, name="filter_lemmas")
]