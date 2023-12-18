from django.urls import include, path

from .views import edit_image
app_name = "treeflow.images"
urlpatterns = [
        path("edit/<uuid:image_id>/",edit_image,name="edit_image")
]