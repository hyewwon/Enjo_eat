from pyexpat import model
from django.db import models

class User(models.Model):
    userid = models.CharField(max_length=50,unique=True,db_column="userid")
    password = models.CharField(max_length=120,db_column="password")

    class Meda:
        db_table = "enjo_user"


class Group(models.Model):
    group_name = models.CharField(db_column="group",max_length=50,null=False)
    group_comment = models.TextField(db_column="group_comment",default="",null=True)
    group_location = models.CharField(db_column="location",max_length=50,default="")
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        db_table = "enjo_group"


class Eatery(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    eatery_name = models.CharField(max_length=30,db_column="eatery_name",null=False)
    eatery_type = models.CharField(max_length=10,db_column="eatery_type",null=False)
    image = models.ImageField(upload_to="eatery_image/", null=True)
    crawling_image = models.CharField(max_length=128,db_column="crawling_image", null=True)
    eatery_real_location = models.CharField(max_length=128,db_column="eatery_real_location", null=False,default="")
    eatery_location = models.CharField(max_length=128,db_column="eatery_location",null=False)
    comment = models.TextField(db_column="comment", default='',null=True)
    
    class Meta:
        db_table = "enjo_eatery"


class Reply(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    eatery = models.ForeignKey(Eatery,on_delete=models.CASCADE)
    reply = models.TextField(db_column="reply",default="",null=True)
    created_at = models.DateTimeField(null=True, db_column='created_at', auto_now_add=True)

    class Meta:
        db_table = "enjo_reply"