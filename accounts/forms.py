from django import forms
from .models import CustomUser,Account,Profile
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.db.models.signals import post_save
from django.dispatch import receiver

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


    # ユーザの登録時にAccountモデルにレコードを追加する
    @receiver(post_save,sender=CustomUser)
    def create_account(sender,**kwargs):
        if kwargs['created']:
            user_account = Account.objects.get_or_create(user=kwargs['instance'])

    # ユーザの登録時にAccountモデルにレコードを追加する
    @receiver(post_save,sender=CustomUser)
    def create_account(sender,**kwargs):
        if kwargs['created']:
            user_profile = Profile.objects.get_or_create(user=kwargs['instance'])


class LoginForm(AuthenticationForm):
    pass

class AccountFrom(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'birthday', 'address', 'tel']
        labels = {
        'name':'お名前',
        'birthday':'お誕生日',
        'address':'ご住所',
        'tel':'お電話番号'}


class ProfileFrom(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'image', 'gender', 'age', 'short_msg', 'comment']
        labels = {
        'nickname':'ニックネーム',
        'image':'画像',
        'gender':'性別',
        'age':'年齢',
        'short_msg':'一言メッセージ',
        'comment':'コメント',
        }
        


