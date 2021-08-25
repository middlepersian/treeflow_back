from django.urls import include, path

app_name = "mpcd.dict"
urlpatterns = [
        path("dict/", include("dict.urls")),

]