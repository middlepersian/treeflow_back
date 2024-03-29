from django.urls import include, path
from treeflow.dict.views.save_sense import save_sense
from treeflow.dict.views.save_lemma import save_lemma

app_name = "treeflow.dict"
urlpatterns = [
        path("save_sense/", save_sense, name="save_sense"),
        path("save_lemma/", save_lemma, name="save_lemma"),
]