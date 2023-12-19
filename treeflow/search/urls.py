from django.urls import path
from . import views

app_name = "treeflow.search"

urlpatterns = [
    path("", views.search_page, name="search"),
    path("results/", views.results_view, name="results"),
]
