from django.urls import path
from . import views

app_name = "treeflow.search"

urlpatterns = [
    path("", views.search_page, name="search"),
    path("change_search_type/", views.change_search_type, name="change_search_type"),
]
