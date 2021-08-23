from django.urls import include, path

app_name = "mpcd.edition"
urlpatterns = [
        path("edition/", include("edition.urls")),

]