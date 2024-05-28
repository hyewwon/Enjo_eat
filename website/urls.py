from django.urls import path
from django.contrib.auth.views import LogoutView
from website.views.auth_views.auth_views import LoginView, JoinView,CheckDupleView, MyPageView, MyGroupView, MyEateryView, HomeView
from website.views.group_views.group_views import GroupManageView, GroupCreateView, GroupEditView
from website.views.eatery_views.eatery_views import EateryManageView, EateryCreateView, EateryEditView, EateryDetailView, EateryReplyView, crawlingImage
from website.views.eatery_selection_views.eatery_selection_views import GroupSelectView, EateryAllSelectView, GetGroupLocationView, EaterySelectView

from django.conf import settings

app_name = "website"

urlpatterns = [
    #auth
    path("",HomeView.as_view(),name="home"),
    path("login/",LoginView.as_view(),name="login"),
    path("join/",JoinView.as_view(), name="join"),
    path("duple/",CheckDupleView.as_view(), name="checkDuple"),
    path('logout/', LogoutView.as_view(next_page='website:home'), name='logout'),
    path("my-group/", MyGroupView.as_view(), name="my_group"),
    path("mypage/", MyPageView.as_view(), name="mypage"),
    path("my-eatery/<int:group_id>/", MyEateryView.as_view(), name="my_eatery"),

    # group
    path("group-manage/",GroupManageView.as_view(), name="group_manage"),
    path("group-create/",GroupCreateView.as_view(), name="group_create"),
    path("group-edit/<int:pk>/",GroupEditView.as_view(),name="group_edit"),
    
    # eatery
    path("eatery-manage/<int:pk>/",EateryManageView.as_view(),name="eatery_manage"),
    path("eatery-create/<int:pk>/",EateryCreateView.as_view(),name="eatery_create"),
    path("eatery-edit/<int:pk>/",EateryEditView.as_view(),name="eatery_edit"),
    path("eatery-detail/<int:pk>/",EateryDetailView.as_view(),name="eatery_detail"),
    path("eatery-reply/<int:pk>/",EateryReplyView.as_view(),name="eatery_reply"),
    path("eatery-image_crawling/",crawlingImage,name="image_crawling"),

    #eatery selection
    path("group-select/",GroupSelectView.as_view(), name="group_select"),
    path("group-all-select/",EateryAllSelectView.as_view(),name="group_all_select"),
    path("get-group-location/",GetGroupLocationView.as_view(),name="get_group_location"),
    path("eatery-select/",EaterySelectView.as_view(),name="eatery_select"),

] 