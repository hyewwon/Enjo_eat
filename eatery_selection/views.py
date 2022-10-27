from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from eatery.models import Group, Eatery
from django.db.models import Q
import random

class GroupSelectView(View):
    def get(self,request:HttpRequest,*args, **kwargs):
        context = {}
        groups = Group.objects.all()
        context["groups"] = groups
        return render(request,"eatery_selection/group_select.html",context)


class EateryAllSelectView(View):
    def get(self,request:HttpRequest,*args, **kwargs):

        context = {}

        return render(request,"eatery_selection/group_all_select.html",context)


class GetGroupLocationView(View):
    
    def get(self,request:HttpRequest,*args, **kwargs):
        context = {}

        try:
            eatery_location = Eatery.objects.all().values("eatery_location")
        except:
            context["success"] = False
            context["message"] = "위치 가져오기 실패"

            return JsonResponse(context)

        temp = set()

        for location in eatery_location:
            temp.add(" ".join(location.get("eatery_location").split(" ")[:-1]))

        context["eatery_location"] = list(temp)
        context["success"] = True

        return JsonResponse(context)


class EaterySelectView(View):

    def get(self,request:HttpRequest,*args, **kwargs):

        group_id = request.GET.get("group_id")
        eatery_type = request.GET.getlist("eatery_type")
        eatery_location = request.GET.get("eatery_location","")

        context = {}

        if group_id:
            eatery = Eatery.objects.filter(group=group_id).values("eatery_name","id","image","crawling_image")
            context["random_eatery"] = random.sample(list(eatery),len(eatery))
            context["group_id"] = group_id

        else:
            eatery = Eatery.objects.filter(
                Q(eatery_location__icontains = eatery_location)&
                Q(eatery_type__in = eatery_type)
                ).values("eatery_name","id","image","crawling_image")

            context["random_eatery"] = random.sample(list(eatery),len(eatery))
            
        return render(request,"eatery_selection/eatery_select.html",context)