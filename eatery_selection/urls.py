from django.urls import path
from .views import GroupSelectView,EateryAllSelectView,GetGroupLocationView,EaterySelectView

from django.conf.urls.static import static
from django.conf import settings

app_name = "Eatery_selection"

urlpatterns = [
    path("group_select/",GroupSelectView.as_view(), name="group_select"),
    path("group_all_select/",EateryAllSelectView.as_view(),name="group_all_select"),
    path("get_group_location/",GetGroupLocationView.as_view(),name="get_group_location"),
    path("eatery_select/",EaterySelectView.as_view(),name="eatery_select"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)