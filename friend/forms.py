from django import forms
from .models import Friend,Message,Group,Posts
from accounts.models import Profile

# class FriendForm(forms.ModelForm):
#     class Meta:
#         model = Friend
#         fields = (
#             'follower',
#             'followed',
#         )

# class MessageForm(forms.ModelForm):
#     class Meta:
#         model = Message
#         fields = (
#             'user.follower',
#             'user.followed',
#             'msg',
#         )

class GroupForm(forms.ModelForm):

    user = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=Friend.objects.none())
    class Meta:
        model = Group
        fields= (
            'name',
            'user',
        )
        labels = {
            'name':'グループ名',
            'user':'友達',
        }

class GroupNameForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = (
            'name',
        )
        labels = {
            'name':'グループ名',
        }


class PostsForm(forms.ModelForm):
    posts = forms.CharField(widget=forms.Textarea(attrs={'cols': '80', 'rows': '2'}))
    class Meta:
        model = Posts
        fields = ['user','photo','posts']
        labels = {
            'user':'ユーザ',
            'photo':'写真',
            'posts':'投稿',
        }

    def __init__(self,user,*args,**kwargs):
        self.l_user=user
        super(PostsForm,self).__init__(*args,**kwargs)
        self.fields['user'].initial=self.l_user