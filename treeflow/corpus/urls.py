from django.urls import include, path

app_name = "treeflow.corpus"
urlpatterns = [
    path("corpus/", include("corpus.urls"))
]
