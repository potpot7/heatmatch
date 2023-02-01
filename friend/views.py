from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView,ListView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from .models import Friend,Room,Message,Group,Posts
from .forms import GroupForm,PostsForm
from accounts.models import CustomUser,Profile

class FriendsView(LoginRequiredMixin, ListView):
    template_name = 'friend/friends.html'
    queryset = Friend.objects.none()
    context_object_name = 'friend_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ログインユーザを取得
        user = Profile.objects.get(user=self.request.user)
        # フォローしているユーザを取得
        follower = Friend.objects.filter(follower=user).select_related('follower').order_by('create_date')
        # フォローされているユーザを取得
        followed = Friend.objects.filter(followed=user).select_related('followed').order_by('create_date')
        # 相互フォローを取得
        # 空のリストを作成
        friends = []
        for fr in follower:
            for fd in followed:
                if fr.followed == fd.follower and fr.follower == fd.followed:
                    friends.append(fr)
        # それぞれの値を格納
        context['follower'] = follower
        context['followed'] = followed
        context['friends'] = friends
        group = Group.objects.filter(user=user)
        context['group'] = group
        return context

class MessageView(LoginRequiredMixin, TemplateView):
    template_name = 'friend/message.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        # urlからユーザを取得
        sender = self.kwargs['pk']
        receiver = self.kwargs['name']
        context['s'] = Profile.objects.get(id=sender)
        context['r'] = Profile.objects.get(id=receiver)
        # チャットルームを作成or取得
        room_a =f"{context['s'].user.username}と{context['r'].user.username}の部屋"
        room_b =f"{context['r'].user.username}と{context['s'].user.username}の部屋"
        if Room.objects.filter(name=room_a).exists():
            room = Room.objects.get(name=room_a)
        else:
            if Room.objects.filter(name=room_b).exists():
                room = Room.objects.get(name=room_b)
            else:
                room = Room.objects.create(name=room_a)
        context['room'] = room
        # 部屋に紐づくメッセージを取得
        context['messages'] = Message.objects.filter(room=context['room'])
        return context
# メッセージ送信処理
    def post(self,request,*args,**kwargs):
        context = self.get_context_data()
        if 'send' in request.POST:
            # 部屋、送信者、メッセージを保存
            form = Message.objects.create(
                room=context['room'],
                user=context['s'],
                msg=request.POST['content'])
        return render(request,self.template_name,context)

class MessageGroupView(LoginRequiredMixin, TemplateView):
    template_name = 'friend/message_group.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        # urlからグループを取得
        r_id = self.kwargs['num']
        user = Profile.objects.get(user=self.request.user)
        context['user'] = user
        # チャットルームを取得
        room = Room.objects.get(id=r_id)
        context['room'] = room
        context['messages'] = Message.objects.filter(room=context['room'])
        return context

    def post(self,request,*args,**kwargs):
        context = self.get_context_data()
        if 'send' in request.POST:
            form = Message.objects.create(
                room=context['room'],
                user=context['user'],
                msg=request.POST['content'])
        return render(request,self.template_name,context)

class GroupView(LoginRequiredMixin,CreateView):
    template_name = 'friend/group.html'
    form_class = GroupForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # ログインユーザを取得
        user = Profile.objects.get(user=self.request.user)
        # フォローしているユーザを取得
        follower = Friend.objects.filter(follower=user).select_related('follower').order_by('create_date')
        # フォローされているユーザを取得
        followed = Friend.objects.filter(followed=user).select_related('followed').order_by('create_date')
        # 相互フォローを取得
        # 空のリストを作成
        friends = []
        for fr in follower:
            for fd in followed:
                if fr.followed == fd.follower and fr.follower == fd.followed:
                    friends.append(fr)
        # 値を格納
        form.fields['user'].choices = [(fr.followed.user.id,fr.followed.nickname) for fr in friends]
        return form

    def post(self, request, *args, **kwargs):
        context = {}
        me = Profile.objects.get(user=request.user)
        # グループが作られたとき
        if 'send' in request.POST:
            # 作成者を取得
            name = request.POST['name']
            users = []
            # 入力されたユーザを取得
            if 'user' in request.POST:
                for u in request.POST.getlist('user'):
                    user = Profile.objects.get(user__id=u)
                    users.append(user)
                users.append(me)
                # 一意になる数字（Roomの件数）を取得
                num=Room.objects.all().count()
                # チャットルームを作成
                if Room.objects.filter(name=name).exists():
                    context['message'] = '同じ名前の部屋があります。'
                    return render(request,self.template_name,context)
                Room.objects.create(name=name)
                # 作成したチャットルームを取得
                room = Room.objects.get(name=name)
                # グループをユーザの数だけ作成
                for u in users:
                    group = Group(
                        room=room,
                        num=num,
                        name=name,
                        user=u,
                    )
                    group.save()
                context['message'] = "グループを作成しました。"
            else:
                context['message'] = "一人以上選択してください。"
        return render(request,self.template_name,context)

class PostsView(LoginRequiredMixin,ListView):
    template_name = 'friend/posts.html'
    context_object_name = 'posts'
    model = Posts
    ordering = '-create_date'

# 共通処理
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'] = PostsForm(user=self.request.user)
        return context

# 投稿処理
    def post(self,request,*args,**kwargs):
        context = self.get_context_data()
        # 投稿ユーザを取得
        user = Profile.objects.get(user=request.user)
        if 'send' in request.POST:
            # 投稿内容を取得、保存
            form = PostsForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
        return render(request,self.template_name,context)