from django.urls import path
from . import views
from . import views_update as vuvuzela

app_name = "treeflow.search"

urlpatterns = [
    path("", views.search_page, name="search"),
    path("demo/", vuvuzela.search_index, name="demo"),
    path("results/", views.results_view, name="results"),
]
