from django.urls import include, path
from treeflow.dict.views.save_sense import save_sense
from treeflow.dict.views.save_lemma import save_lemma
from django.views.generic import TemplateView
from treeflow.dict.views.lemma_details import lemma_details

from treeflow.dict.views.lemmas_list import lemmas_list

app_name = "treeflow.dict"
urlpatterns = [
        path("save_sense/", save_sense, name="save_sense"),
        path("save_lemma/", save_lemma, name="save_lemma"),
        path("dictionary/", lemmas_list, name="dictionary"),
        path("dictionary/<uuid:lemma_id>/", lemma_details, name="lemma_details"),
]