from django.urls import include, path

app_name = "mpcd.codex"
urlpatterns = [
        path("codex/", include("codex.urls")),

]