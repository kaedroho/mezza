from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path

from .auth import views as auth_views
from .ideas import views as ideas_views
from .media import views as media_views
from .projects import views as projects_views
from .spaces.decorators import space
from .utils.urlpatterns import decorate_urlpatterns

urlpatterns_space = [
    path(
        "<slug:space_slug>/projects/",
        projects_views.projects_index,
        name="projects_index",
    ),
    path(
        "<slug:space_slug>/projects/create/",
        projects_views.projects_create,
        name="projects_create",
    ),
    path(
        "<slug:space_slug>/projects/<int:project_id>/",
        projects_views.project_detail,
        name="project_detail",
    ),
    path(
        "<slug:space_slug>/projects/<int:project_id>/edit/",
        projects_views.project_edit,
        name="project_edit",
    ),
    path(
        "<slug:space_slug>/projects/<int:project_id>/assets/upload/",
        media_views.asset_upload,
        name="asset_upload",
    ),
    path(
        "<slug:space_slug>/projects/<int:project_id>/assets/choose/",
        media_views.asset_choose_for_project,
        name="asset_choose_for_project",
    ),
    path(
        "<slug:space_slug>/projects/ideas/", ideas_views.ideas_index, name="ideas_index"
    ),
    path(
        "<slug:space_slug>/projects/ideas/create/",
        ideas_views.ideas_create,
        name="ideas_create",
    ),
    path(
        "<slug:space_slug>/projects/ideas/<int:idea_id>/start-production/",
        ideas_views.ideas_start_production,
        name="ideas_start_production",
    ),
    path("<slug:space_slug>/media/", media_views.asset_index, name="asset_index"),
    path(
        "<slug:space_slug>/media/<int:asset_id>/",
        media_views.asset_detail,
        name="asset_detail",
    ),
    path(
        "<slug:space_slug>/media/upload/",
        media_views.asset_upload,
        name="asset_upload",
    ),
]

# Put any URLs that require authentication in this list.
urlpatterns_auth = [
    path("", auth_views.login_redirect, name="login_redirect"),
    path("admin/", admin.site.urls),
    path("", include(decorate_urlpatterns(urlpatterns_space, space))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Put any URLs that do not require authentication in this list.
urlpatterns_noauth = [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("login-temporary/", auth_views.login_temporary, name="login_temporary"),
]

urlpatterns = urlpatterns_noauth + decorate_urlpatterns(
    urlpatterns_auth, login_required
)
