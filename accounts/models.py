from django.db import models
from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser,UserManager
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver

# ユーザマネージャーの定義================================================
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)


# カスタムユーザの定義================================================
class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"),
        unique=True,
        blank=True)
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

@receiver(post_save, sender=CustomUser)
def create_profile(sender, **kwargs):
    """ 新ユーザー作成時に空のprofileも作成する """
    if kwargs['created']:
        account = Account.objects.get_or_create(user=kwargs['instance'])
        profile = Profile.objects.get_or_create(user=kwargs['instance'])

# 関数の定義=========================================================

# genderの選択肢
gender_choice=(
    ('男性','男性'),
    ('女性','女性'),
    ('その他','その他'),
)

# モデルの定義=======================================================
# アカウントモデル
class Account(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='account_user')
    name = models.CharField(max_length=60,blank=True,null=True)
    birthday = models.DateField(blank=True,null=True)
    address = models.TextField(max_length=255,blank=True,null=True)
    tel = models.CharField(max_length=15,blank=True,null=True)
    create_date = models.DateTimeField(auto_now_add=True,editable=False)
    delete_date = models.DateTimeField(blank=True,null=True,editable=False)

    def __str__(self):
        return self.user.username

# プロフィールモデル
class Profile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='profile_user')
    nickname = models.CharField(max_length=32,blank=True,null=True,default="名無し")
    image = models.ImageField(upload_to='img/',blank=True,null=True)
    gender = models.CharField(max_length=3,choices=gender_choice,blank=True,null=True)
    age = models.IntegerField(blank=True,null=True)
    short_msg = models.CharField(max_length=32,blank=True,null=True,default="一言メッセージ")
    comment = models.TextField(max_length=600,blank=True,null=True)
    create_date = models.DateTimeField(auto_now_add=True,editable=False)
    delete_date = models.DateTimeField(blank=True,null=True,editable=False)

    def __str__(self):
        return self.user.username

# AKAZE画像保存用
class ComparisonImage(models.Model):
    tgt = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='target_user')
    cmp = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='comparison_user')
    ret = models.FloatField(blank=True,null=True)
    images = models.ImageField(upload_to='img/',blank=True,null=True)
    create_date = models.DateTimeField(auto_now_add=True,editable=False)
    
    def __str__(self):
        return f'{self.tgt} to {self.cmp}'
    
    class Meta:
        ordering = ['-create_date']