from django.urls import path
from .views import search_page, change_search_type

app_name = "treeflow.search"

urlpatterns = [
    path("", search_page, name="search_page"),
    path("change_search_type/", change_search_type, name="change_search_type")
]
