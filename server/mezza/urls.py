from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path

from .auth import views as auth_views
from .files import views as files_views
from .workspaces.decorators import workspace
from .utils.urlpatterns import decorate_urlpatterns

urlpatterns_workspace = [
    path("<slug:workspace_slug>/files/", files_views.file_index, name="file_index"),
    path(
        "<slug:workspace_slug>/files/<int:file_id>/",
        files_views.file_detail,
        name="file_detail",
    ),
    path(
        "<slug:workspace_slug>/files/upload/",
        files_views.file_upload,
        name="file_upload",
    ),
]

# Put any URLs that require authentication in this list.
urlpatterns_auth = [
    path("", auth_views.login_redirect, name="login_redirect"),
    path("admin/", admin.site.urls),
    path("", include(decorate_urlpatterns(urlpatterns_workspace, workspace))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Put any URLs that do not require authentication in this list.
urlpatterns_noauth = [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("login-temporary/", auth_views.login_temporary, name="login_temporary"),
]

urlpatterns = urlpatterns_noauth + decorate_urlpatterns(
    urlpatterns_auth, login_required
)
