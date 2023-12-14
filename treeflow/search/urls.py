from django.urls import path
from . import views

app_name = "treeflow.search"

urlpatterns = [
    path("", views.search_page, name="search"),
    path("toggle_type/", views.change_search_type, name="toggle_type"),
    path("results/", views.results_view, name="results"),
]
