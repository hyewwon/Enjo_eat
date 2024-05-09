from django.views import View
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.db import transaction
from django.contrib.auth.hashers import check_password, make_password
from website.models import User, Group, Eatery
from decimal import Decimal
import json

class HomeView(View):
    def get(self,request:HttpRequest,*args, **kwargs):
        context = {}
        eatery = Eatery.objects.all().values("id","user__userid","comment","eatery_name","image","crawling_image")
        context["eatery"] = eatery

        return render(request,"home.html",context)


class LoginView(View):
    def get(self,request:HttpRequest,*args, **kwargs):
        return render(request,"auth/login.html")

    def post(self,request:HttpRequest,*args, **kwargs):
        context = {}
        userid = request.POST.get("userid")
        password = request.POST.get("password")
        try:
            user = User.objects.get(userid=userid)

            if check_password(password,user.password):
                request.session["userid"] = user.userid
                context["check"] = "success"
            else:
                context["check"] = "fail"
        except User.DoesNotExist:
            context["check"] = "fail"
        except:
            context["success"] = False
            return JsonResponse(context)

        context["success"] = True
        return JsonResponse(context)


class LogoutView(View):
    def get(self,request:HttpRequest,*args, **kwargs):
        if request.session.get("userid"):
            del(request.session["userid"])

        return redirect("/")


class JoinView(View):
    def get(self,request:HttpRequest,*args, **kwargs):
        return render(request,"auth/join.html")
    
    def post(self,request:HttpRequest,*args, **kwargs):
        userid = request.POST.get("userid")
        password = request.POST.get("password")

        with transaction.atomic():
            user = User(
                userid = userid,
                password = make_password(password)
            )
            user.save()

        return redirect("/")


class CheckDupleView(View):
    def post(self,request:HttpRequest,*args, **kwargs):
        context = {}
        request.POST = json.loads(request.body)
        userid = request.POST.get("userid")

        context["exist"] = True
        try:
            User.objects.get(userid = userid)
        except:
            context["exist"] = False
        
        context["success"] = True

        return JsonResponse(context)


class MyPageView(View):
    def get(self, request:HttpRequest, *args, **kwargs):
        userid = request.session.get("userid")
        if not userid:
            return render(request,"auth/no_login.html",{'next':'website:login'})
        return render(request, "auth/mypage.html")
    

class MyGroupView(View):
    def get(self, request:HttpRequest, *args, **kwargs):
        userid = request.session.get("userid")
        if not userid:
            return render(request,"auth/no_login.html",{'next':'website:login'})
        
        context= {}
        user = User.objects.get(userid = userid)
        groups = Group.objects.filter(user = user)
        context['groups'] = groups
        return render(request, "auth/my_group.html", context)
        

class MyEateryView(View):
    def get(self, request:HttpRequest, *args, **kwargs):
        context= {}
        userid = request.session.get("userid")
        if not userid:
            return render(request, "auth/no_login.html", {"next":"website:login"})
        pk = kwargs.get("group_id")
        eateries = Eatery.objects.filter(group = pk)
        context["eateries"] = eateries
        return render(request, "auth/my_eatery.html", context)

