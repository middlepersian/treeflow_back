from django.urls import path
from .views import search_page

app_name = "treeflow.search"

urlpatterns = [
    path("", search_page, name="search_page"),
]
