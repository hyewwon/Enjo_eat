from django.views import View
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count
from django.db import transaction
from website.models import Group
import json

class GroupManageView(LoginRequiredMixin, View):
    '''
        그룹 목록
    '''
    login_url="website:login"
    def get(self,request:HttpRequest,*args, **kwargs):
        context = {}
        groups = Group.objects.annotate(
            count = Count("eatery")
        ).values("id", "group_name", "group_comment", "group_location", "open_flag", "count")
        context["groups"] = groups
        return render(request,"eatery/group_manage.html",context)

    
class GroupCreateView(LoginRequiredMixin, View):
    '''
        그룹 생성
    '''
    login_url="website:login"
    def get(self,request:HttpRequest,*args, **kwargs):
        return render(request,"eatery/group_create.html")

    def post(self,request:HttpRequest,*args, **kwargs):
        context={}
        request.POST = json.loads(request.body)
        group_name = request.POST.get("group_name")
        group_comment = request.POST.get("group_comment")
        group_location = request.POST.get("group_location")
        open_flag = request.POST.get("open_flag")

        user = get_object_or_404(User,username=request.user)
        try:
            with transaction.atomic():
                group = Group(
                    user = user,
                    group_name = group_name,
                    group_comment = group_comment,
                    group_location = group_location,
                    open_flag = open_flag
                )
                group.save()
        except:
            return JsonResponse({"message":"테마 생성 오류.. 관리자에게 문의해주세요!"}, status=400)
        
        context["url"] = reverse("website:eatery_create", kwargs={"pk":group.id})
        return JsonResponse(context, status=202)

class GroupEditView(LoginRequiredMixin, View):
    '''
        그룹 수정
    '''
    login_url="website:login"
    def get(self,request:HttpRequest,*args, **kwargs):
        context = {}
        pk = kwargs.get("pk")
        group = get_object_or_404(Group,pk=pk)
        context["group"] = group
        return render(request,"eatery/group_edit.html",context)

    def post(self,request:HttpRequest,*args, **kwargs):
        pk = kwargs.get("pk")
        group_name = request.POST.get("name")
        group_location = request.POST.get("location")
        group_comment = request.POST.get("comment")

        group = get_object_or_404(Group,pk=pk)
        
        group.group_name = group_name
        group.group_location = group_location
        group.group_comment = group_comment

        group.save()

        return redirect("/eatery/group_manage/")

    def delete(self,request:HttpRequest,*args, **kwargs):
        context = {}
        request.POST= json.loads(request.body)
        group_pk = request.POST.get("group_pk")
        group = get_object_or_404(Group,pk=group_pk)
        try:
            group.delete()
        except:
            context["success"] = False

        context["success"] = True

        return JsonResponse(context)
