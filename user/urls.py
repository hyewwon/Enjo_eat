from django.urls import path
from .views import LoginView, JoinView,CheckDupleView,LogoutView

from django.conf.urls.static import static
from django.conf import settings

app_name = "User"

urlpatterns = [
    path("login/",LoginView.as_view(),name="login"),
    path("join/",JoinView.as_view(), name="join"),
    path("duple/",CheckDupleView.as_view(), name="checkDuple"),
    path("logout/",LogoutView.as_view(), name="logout"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)