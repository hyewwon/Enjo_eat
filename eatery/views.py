from django.views import View
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.db import transaction
from .models import Eatery, Reply,User,Group
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import urllib.request
import time


class HomeView(View):
    def get(self,request:HttpRequest,*args, **kwargs):
        context = {}
        eatery = Eatery.objects.all().values("id","user__userid","comment","eatery_name","image","crawling_image")
        context["eatery"] = eatery

        return render(request,"home.html",context)


class GroupManageView(View):
    def get(self,request:HttpRequest,*args, **kwargs):
        if not request.session.get('userid'):

            return render(request,"user/no_login.html",{'next':'User:login'})

        context = {}
        groups = Group.objects.all()
        context["groups"] = groups
        return render(request,"eatery/group_manage.html",context)

    
class GroupCreateView(View):

    def get(self,request:HttpRequest,*args, **kwargs):
        if not request.session.get("userid"):

            return render(request,"user/no_login.html",{"next":"User:login"})
        
        return render(request,"eatery/group_create.html")

    def post(self,request:HttpRequest,*args, **kwargs):

        group_name = request.POST.get("name")
        group_comment = request.POST.get("comment")
        group_location = request.POST.get("location")

        user = get_object_or_404(User,userid=request.session["userid"])
        with transaction.atomic():
            group = Group(
                group_name = group_name,
                group_comment = group_comment,
                group_location = group_location,
                user = user
            )

            group.save()

        return redirect(f"/eatery/eatery_create/{group.id}/")

class GroupEditView(View):

    def get(self,request:HttpRequest,*args, **kwargs):
        if not request.session.get("userid"):

            return render(request,"user/no_user.html",{"next":"User:login"})

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


class EateryManageView(View):
    def get(self,request:HttpRequest,*args, **kwargs):

        if not request.session.get('userid'):

            return render(request,"user/no_login.html",{'next':'User:login'})

        context = {}
        group_pk = kwargs.get("pk")
        eatery = Eatery.objects.filter(group=group_pk)
        context["group_pk"] = group_pk
        context["eatery"] = eatery

        return render(request,"eatery/eatery_manage.html",context)


class EateryCreateView(View):

    def get(self, request:HttpRequest,*args, **kwargs):
        if not request.session.get('userid'):

            return render(request,"user/no_login.html",{'next':'User:login'})

        context = {}
        group_pk = kwargs.get("pk")
        group = Group.objects.get(pk=group_pk)
        context["group_pk"] = group_pk
        context["group_location"] = group.group_location

        return render(request,"eatery/eatery_create.html",context)


    def post(self,request:HttpRequest,*args, **kwargs):

        group_pk = kwargs.get("pk")
        eatery_name = request.POST.get("eatery_name")
        eatery_type = request.POST.get("eatery_type")
        eatery_location = request.POST.get("show_location")
        eatery_real_location = request.POST.get("eatery_real_location")
        image = request.FILES.get("user_image",None)
        crawl_image = request.POST.get("crawl_image")
        comment = request.POST.get("comment")

        group = get_object_or_404(Group,pk=group_pk)
        user = get_object_or_404(User,userid=request.session["userid"])

        with transaction.atomic():
            eatery = Eatery(
                group=group,
                user=user,
                eatery_name=eatery_name,
                eatery_type=eatery_type,
                eatery_location=eatery_location,
                image=image,
                eatery_real_location = eatery_real_location,
                crawling_image = crawl_image,
                comment = comment
            )

            eatery.save()

        return redirect(f"/eatery/eatery_manage/{group.pk}")

class EateryDetailView(View):
    def get(self,request:HttpRequest,*args, **kwargs):
        if not request.session.get('userid'):

            return render(request,"user/no_login.html",{'next':'home'})

        context = {}
        pk = kwargs.get("pk")
        
        eatery = get_object_or_404(Eatery,pk=pk)
        try:

            reply_list = Reply.objects.filter(eatery=eatery).order_by("-created_at")
            count_reply = len(reply_list)
        except:
            context["blank"] = True

        context["group_pk"] = eatery.group.id
        context["eatery"] = eatery

        context["reply_list"] = render_to_string("eatery/reply_list.html",{
            "reply_list":reply_list,
            "count_reply":count_reply,
            "logged_id":request.session.get("userid")})
    
        return render(request,"eatery/eatery_detail.html",context)

    def delete(self,request:HttpRequest,*args, **kwargs):
        context = {}
        pk = kwargs.get("pk")
        eatery = get_object_or_404(Eatery,pk = pk)
        try:
            eatery.delete()
        except:
            context["success"] = False
            return JsonResponse(context)
            
        context["success"] = True
        return JsonResponse(context)



class EateryEditView(View):
    def get(self,request:HttpRequest,*args, **kwargs):
        context = {}
        pk = kwargs.get("pk")

        eatery = get_object_or_404(Eatery,pk=pk)
        context["eatery"] = eatery

        return render(request,"eatery/eatery_edit.html",context)

    def post(self,request:HttpRequest,*args, **kwargs):
        context = {}

        pk = kwargs.get("pk")
        eatery_name = request.POST.get("eatery_name")
        eatery_type = request.POST.get("eatery_type")
        comment = request.POST.get("comment")
        eatery_location = request.POST.get("show_location")
        eatery = get_object_or_404(Eatery,pk=pk)

        eatery.eatery_name = eatery_name
        eatery.eatery_type = eatery_type
        eatery.comment = comment
        eatery.eatery_location = eatery_location

        eatery.save()

        return redirect(f"/eatery/eatery_detail/{pk}/")


class EateryReplyView(View):

    def post(self,request:HttpRequest,*args, **kwargs):
        context = {}
        pk = kwargs.get("pk")
        request.POST = json.loads(request.body)
        userid = request.POST.get("userid")
        reply = request.POST.get("reply")
        logged_id = request.session.get("userid")
        eatery = get_object_or_404(Eatery,pk=pk)
        user = get_object_or_404(User,userid=userid)
        try:
            reply = Reply(
                eatery = eatery,
                user = user,
                reply = reply
            )
            reply.save()
        except:
            context["success"] = False

            return JsonResponse(context)

        context["success"] = True

        reply_list = Reply.objects.filter(eatery=eatery).order_by("-created_at")
        count_reply = len(reply_list)

        context["reply_list"] = render_to_string("eatery/reply_list.html",{
            "reply_list":reply_list,
            "count_reply":count_reply,
            "logged_id":logged_id
            })

        return JsonResponse(context)

    

    def delete(self,request:HttpRequest,*args, **kwargs):
        context = {}
        request.POST = json.loads(request.body)

        pk = kwargs.get("pk")
        reply_id = request.POST.get("reply_id")
        reply = get_object_or_404(Reply,id=reply_id)
        eatery = Eatery.objects.get(pk=pk)
        logged_id = request.session.get("userid")
        try:

            reply.delete()

            reply_list = Reply.objects.filter(eatery = eatery).order_by("-created_at")
            count_reply = len(reply_list)
        except:
            context["success"] = False
        
        context["success"] = True
        context["reply_list"] = render_to_string("eatery/reply_list.html",{
            "reply_list":reply_list,
            "count_reply":count_reply,
            "logged_id":logged_id})

        return JsonResponse(context)


def crawlingImage(request):

    context = {}
    image_title = request.GET.get("crawl_image_title")

    image_url = f"C:\pythonProj_board\enjo_eat\static\crawling_image\{image_title}.jpg"
    driver_path = r'C:\pythonProj_board\chromedriver.exe'



    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(driver_path,options=options)
    
    driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl") 
    elem = driver.find_element(By.CSS_SELECTOR,".gLFyf.gsfi")
    elem.send_keys(image_title)
    elem.send_keys(Keys.RETURN)

    image = driver.find_element(By.CSS_SELECTOR,".rg_i.Q4LuWd")

    image.click()
    time.sleep(4)

    try:
        imgUrl = driver.find_element(By.XPATH,'//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img')\
            .get_attribute('src')
    except:
        context["success"] = False
        context["message"] = "크롤링 실패, 다시 시도해 주세요..."

        return JsonResponse(context)
    
    urllib.request.urlretrieve(imgUrl, image_url)

    driver.close()

    temp_list = image_url.split("\\")

    if "C:" in temp_list:
        temp_list.remove("C:")
    if "pythonProj_board" in temp_list:
        temp_list.remove("pythonProj_board")
    if "enjo_eat" in temp_list:
        temp_list.remove("enjo_eat")
        
    image_url = "/".join(temp_list)

    print(f"========={image_url}========")

    context["success"] = True
    context["image_url"] = image_url

    return JsonResponse(context)
