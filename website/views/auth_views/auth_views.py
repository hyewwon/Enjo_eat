from django.views import View
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db import transaction
from website.models import Group, Eatery
import json

class HomeView(View):
    '''
        메인 페이지
    '''
    def get(self,request:HttpRequest,*args, **kwargs):
        context = {}
        eatery = Eatery.objects.all().values("id","user__username","comment","eatery_name","image","crawling_image")
        context["eatery"] = eatery

        return render(request,"home.html",context)


class LoginView(View):
    '''
        로그인
    '''
    def get(self,request:HttpRequest,*args, **kwargs):
        if request.user.is_authenticated:
            return redirect('website:home')
        return render(request,"auth/login.html")

    def post(self,request:HttpRequest,*args, **kwargs):
        context = {}
        userid = request.POST.get("userid")
        password = request.POST.get("password")
        user = authenticate(username=userid, password=password)
        if user:
            login(request, user)
            return JsonResponse(context, status=201)
        
        context["message"] = "아이디 혹은 비밀번호가 다릅니다."
        return JsonResponse(context, status=400)
    

class JoinView(View):
    '''
        회원가입
    '''
    def get(self,request:HttpRequest,*args, **kwargs):
        if request.user.is_authenticated:
            return redirect('website:home')
        return render(request,"auth/join.html")
    
    def post(self,request:HttpRequest,*args, **kwargs):
        userid = request.POST.get("userid")
        password = request.POST.get("password")
        
        if len(userid) < 5:
            return JsonResponse({"message" : "아이디는 5글자 이상입니다."}, status=400)
        if len(password) < 5:
            return JsonResponse({"message" : "비밀번호는 5글자 이상입니다."}, status=400)
        try:
            User.objects.get(username = userid)
            return JsonResponse({"message" : "중복된 아이디 입니다."}, status=400)
        except:
            pass
        try:
            with transaction.atomic():
                User.objects.create_user(
                    username = userid,
                    password=password
                )
        except:
            return JsonResponse({"message" : "가입 오류 발생.. 관리자에게 문의해주세요."}, status=400)
        
        return JsonResponse({"message":"성공"}, status=200)


class CheckDupleView(View):
    '''
        아이디 중복 검사
    '''
    def post(self,request:HttpRequest,*args, **kwargs):
        context = {}
        request.POST = json.loads(request.body)
        userid = request.POST.get("userid")

        try:
            User.objects.get(username = userid)
        except:
            context["exist"] = False
            return JsonResponse(context, status=200)

        context["exist"] = True
        return JsonResponse(context, status=200)


class MyPageView(LoginRequiredMixin, View):
    '''
        마이 페이지
    '''
    login_url="website:login"
    def get(self, request:HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('website:home')
        return render(request, "auth/mypage.html")
    

class MyGroupView(LoginRequiredMixin, View):
    login_url="website:login"
    def get(self, request:HttpRequest, *args, **kwargs):
        context= {}
        user = User.objects.get(userid = request.user.username)
        groups = Group.objects.filter(user = user)
        context['groups'] = groups
        return render(request, "auth/my_group.html", context)
        

class MyEateryView(LoginRequiredMixin, View):
    login_url="website:login"
    def get(self, request:HttpRequest, *args, **kwargs):
        context= {}
        pk = kwargs.get("group_id")
        eateries = Eatery.objects.filter(group = pk)
        context["eateries"] = eateries
        return render(request, "auth/my_eatery.html", context)

