from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from treeflow.views.publications import zotero_view
from strawberry.django.views import AsyncGraphQLView, GraphQLView


urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    path("contact/", TemplateView.as_view(template_name="pages/contact.html"), name="contact"),
    path("publications/",zotero_view, name="publications"),
    path("methodology/", TemplateView.as_view(template_name="pages/methodology.html"), name="methodology"),
    path("resources/", TemplateView.as_view(template_name="pages/resources.html"), name="resources"),
    path("team/", TemplateView.as_view(template_name="pages/team.html"), name="team"),
    path('corpus/', include('treeflow.corpus.urls', namespace='corpus')),
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("treeflow.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),


    # Your stuff: custom urls includes go here

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),

    ]

    if "django_browser_reload" in settings.INSTALLED_APPS:
        import django_browser_reload
        urlpatterns = [path("__reload__/", include(django_browser_reload.urls))] + urlpatterns

    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
