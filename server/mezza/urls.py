from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views
from .auth import views as auth_views
from .utils.urlpatterns import decorate_urlpatterns

# Put any URLs that require authentication in this list.
urlpatterns_auth = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Put any URLs that do not require authentication in this list.
urlpatterns_noauth = [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("login-temporary/", auth_views.login_temporary, name="login_temporary"),
]

urlpatterns = urlpatterns_noauth + decorate_urlpatterns(
    urlpatterns_auth, login_required
)
