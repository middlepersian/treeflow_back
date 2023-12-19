from django.urls import include, path

from .views import edit_image, create_image,delete_image,change_source_for_image
app_name = "treeflow.images"
urlpatterns = [
        path("edit/<uuid:image_id>/",edit_image,name="edit_image"),
        path("delete/<uuid:image_id>/",delete_image,name="delete_image"),
        path("create/",create_image,name="create_image"),
        path("changeSource/<uuid:image_id>/",change_source_for_image,name="change_source_for_image")

]