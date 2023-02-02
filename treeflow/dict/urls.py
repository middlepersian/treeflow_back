from django.urls import include, path

app_name = "treeflow.dict"
urlpatterns = [
        path("dict/", include("dict.urls")),

]