from django.urls import include, path

app_name = "mpcd.corpus"
urlpatterns = [
    path("corpus/", include("corpus.urls"))
]
