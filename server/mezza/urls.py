from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path

from .utils.urlpatterns import decorate_urlpatterns
from .views import auth as auth_views
from .views import files as files_views
from .views import projects as projects_views

# Put any URLs that require authentication in this list.
urlpatterns_auth = [
    path("admin/", admin.site.urls),
    path("projects/", projects_views.index, name="projects_index"),
    path(
        "projects/create/<slug:pipeline_slug>/<slug:stage_id>/",
        projects_views.create,
        name="projects_create",
    ),
    path("files/<slug:type>/", files_views.index, name="files_index"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Put any URLs that do not require authentication in this list.
urlpatterns_noauth = [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("login-temporary/", auth_views.login_temporary, name="login_temporary"),
]

urlpatterns = urlpatterns_noauth + decorate_urlpatterns(
    urlpatterns_auth, login_required
)
