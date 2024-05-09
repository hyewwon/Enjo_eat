from django.views import View
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import transaction
from website.models import Group
import json

class GroupManageView(LoginRequiredMixin, View):
    login_url="website:login"
    def get(self,request:HttpRequest,*args, **kwargs):
        context = {}
        groups = Group.objects.all()
        context["groups"] = groups
        return render(request,"eatery/group_manage.html",context)

    
class GroupCreateView(LoginRequiredMixin, View):
    login_url="website:login"
    def get(self,request:HttpRequest,*args, **kwargs):
        return render(request,"eatery/group_create.html")

    def post(self,request:HttpRequest,*args, **kwargs):
        group_name = request.POST.get("name")
        group_comment = request.POST.get("comment")
        group_location = request.POST.get("location")

        user = get_object_or_404(User,username=request.user)
        with transaction.atomic():
            group = Group(
                group_name = group_name,
                group_comment = group_comment,
                group_location = group_location,
                user = user
            )
            group.save()

        return redirect(f"/eatery/eatery_create/{group.id}/")

class GroupEditView(LoginRequiredMixin, View):
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
