from django.urls import include, path
from treeflow.dict.views.save_sense import save_sense

app_name = "treeflow.dict"
urlpatterns = [
        path("save_sense/", save_sense, name="save_sense"),
]