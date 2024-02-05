from django.urls import path
from .views import LoginView, JoinView,CheckDupleView,LogoutView, MyPageView, MyGroupView, MyEateryView

from django.conf.urls.static import static
from django.conf import settings

app_name = "User"

urlpatterns = [
    path("login/",LoginView.as_view(),name="login"),
    path("join/",JoinView.as_view(), name="join"),
    path("duple/",CheckDupleView.as_view(), name="checkDuple"),
    path("logout/",LogoutView.as_view(), name="logout"),
    path("mypage/", MyPageView.as_view(), name="mypage"),
    path("my-group/", MyGroupView.as_view(), name="my_group"),
    path("my-eatery/<int:group_id>/", MyEateryView.as_view(), name="my_eatery"),

] 