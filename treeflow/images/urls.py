from django.urls import include, path

app_name = "treeflow.images"
urlpatterns = [
        path("images/", include("images.urls")),

]