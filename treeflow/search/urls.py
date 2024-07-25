from django.urls import path

from treeflow.search.render_info_modal import render_info_modal

from . import views

app_name = "treeflow.search"

urlpatterns = [
    path("", views.search_page, name="search"),
    path("results/", views.results_view, name="results"),
    path("info/", render_info_modal, name="info"),
]
