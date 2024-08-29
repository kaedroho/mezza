from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path

from .media import views as media_views
from .auth import views as auth_views
from .ideas import views as ideas_views
from .projects import views as projects_views
from .utils.urlpatterns import decorate_urlpatterns

# Put any URLs that require authentication in this list.
urlpatterns_auth = [
    path("admin/", admin.site.urls),
    path("", projects_views.projects_index, name="projects_index"),
    path(
        "stage/<slug:stage_slug>/",
        projects_views.projects_stage_index,
        name="projects_stage_index",
    ),
    path(
        "create/<slug:stage_slug>/",
        projects_views.projects_create,
        name="projects_create",
    ),
    path(
        "project/<int:project_id>/",
        projects_views.project_detail,
        name="project_detail",
    ),
    path(
        "project/<int:project_id>/assets/upload/",
        media_views.asset_upload,
        name="asset_upload",
    ),
    path("ideas/", ideas_views.ideas_index, name="ideas_index"),
    path("ideas/create/", ideas_views.ideas_create, name="ideas_create"),
    path(
        "ideas/<int:idea_id>/start-production/",
        ideas_views.ideas_start_production,
        name="ideas_start_production",
    ),
    path("media/", media_views.asset_index, name="asset_index"),
    path(
        "media/<slug:library_id>/",
        media_views.asset_index,
        name="asset_index",
    ),
    path(
        "media/<int:library_id>/upload/",
        media_views.asset_upload,
        name="asset_upload",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Put any URLs that do not require authentication in this list.
urlpatterns_noauth = [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("login-temporary/", auth_views.login_temporary, name="login_temporary"),
]

urlpatterns = urlpatterns_noauth + decorate_urlpatterns(
    urlpatterns_auth, login_required
)
