from django.db import models
from accounts.models import CustomUser


# 関数の定義=============================================================


# モデルの定義=============================================================
# コンテンツカテゴリモデル
class Contents(models.Model):
    c_id = models.AutoField(primary_key=True,unique=True)
    main_categ = models.CharField(max_length=255,blank=True,null=True)
    sub_categ = models.CharField(max_length=255,blank=True,null=True)
    contents_name = models.CharField(max_length=255,blank=True,null=True)
    create_date = models.DateTimeField(auto_now_add=True,editable=True)

    def __str__(self):
        return self.contents_name

# 質問モデル
class Question(models.Model):
    q_id = models.AutoField(primary_key=True,unique=True)
    q_title = models.CharField(max_length=255,blank=True,null=True)
    q1 = models.CharField(max_length=255,blank=True,null=True)
    q2 = models.CharField(max_length=255,blank=True,null=True)
    q3 = models.CharField(max_length=255,blank=True,null=True)
    q4 = models.CharField(max_length=255,blank=True,null=True)
    q5 = models.CharField(max_length=255,blank=True,null=True)
    create_date = models.DateTimeField(auto_now_add=True,editable=True)

    def __str__(self):
        return self.q_title

class Answer(models.Model):
    a_id = models.AutoField(primary_key=True,unique=True)
    user = models.ForeignKey(CustomUser,to_field='email',on_delete=models.CASCADE)
    c_id = models.ForeignKey(Contents,to_field='c_id',on_delete=models.CASCADE)
    q_id = models.ForeignKey(Question,to_field='q_id',on_delete=models.CASCADE)
    a1 = models.BooleanField(default=False)
    a2 = models.BooleanField(default=False)
    a3 = models.BooleanField(default=False)
    a4 = models.BooleanField(default=False)
    a5 = models.BooleanField(default=False)
    a_val = models.IntegerField(blank=True,null=True)
    create_date = models.DateTimeField(auto_now_add=True,editable=True)

    def __str__(self):
        return f"{self.user.username} : {self.q_id.q_id} / {self.a_id}"
