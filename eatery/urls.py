from django.urls import path
from .views import GroupManageView,GroupCreateView,GroupEditView,EateryCreateView,EateryEditView,EateryManageView, EateryDetailView, EateryReplyView,crawlingImage

from django.conf.urls.static import static
from django.conf import settings

app_name = "Eatery"

urlpatterns = [
    path("group_manage/",GroupManageView.as_view(), name="group_manage"),
    path("group_create/",GroupCreateView.as_view(), name="group_create"),
    path("group_edit/<int:pk>/",GroupEditView.as_view(),name="group_edit"),
    path("eatery_manage/<int:pk>/",EateryManageView.as_view(),name="eatery_manage"),
    path("eatery_create/<int:pk>/",EateryCreateView.as_view(),name="eatery_create"),
    path("eatery_edit/<int:pk>/",EateryEditView.as_view(),name="eatery_edit"),
    path("eatery_detail/<int:pk>/",EateryDetailView.as_view(),name="eatery_detail"),
    path("eatery_reply/<int:pk>/",EateryReplyView.as_view(),name="eatery_reply"),
    path("eatery_image_crawling/",crawlingImage,name="image_crawling"),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)