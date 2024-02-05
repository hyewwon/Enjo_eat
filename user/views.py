from django.views import View
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.db import transaction
from django.contrib.auth.hashers import check_password, make_password
from eatery.models import User, Group, Eatery
from decimal import Decimal
import json

class LoginView(View):
    def get(self,request:HttpRequest,*args, **kwargs):
        return render(request,"user/login.html")

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
        return render(request,"user/join.html")
    
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
            return render(request,"user/no_login.html",{'next':'User:login'})
        return render(request, "user/mypage.html")
    

class MyGroupView(View):
    def get(self, request:HttpRequest, *args, **kwargs):
        userid = request.session.get("userid")
        if not userid:
            return render(request,"user/no_login.html",{'next':'User:login'})
        
        context= {}
        user = User.objects.get(userid = userid)
        groups = Group.objects.filter(user = user)
        context['groups'] = groups
        return render(request, "user/my_group.html", context)
        

class MyEateryView(View):
    def get(self, request:HttpRequest, *args, **kwargs):
        context= {}
        userid = request.session.get("userid")
        if not userid:
            return render(request, "user/no_login.html", {"next":"User:login"})
        pk = kwargs.get("group_id")
        eateries = Eatery.objects.filter(group = pk)
        context["eateries"] = eateries
        return render(request, "user/my_eatery.html", context)

