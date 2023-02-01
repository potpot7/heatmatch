from django.shortcuts import render,redirect
from django.urls import reverse_lazy,reverse
from .forms import SignupForm, LoginForm,AccountFrom,ProfileFrom
from django.contrib.auth import login
from django.core.paginator import Paginator
from .models import CustomUser,Account,Profile,ComparisonImage
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, CreateView,UpdateView,ListView,View,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
import cv2
from PIL import Image
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
from datetime import datetime
from django.conf import settings
from q_a.views import paginate_query

# ユーザ作成
class MySignupView(FormView):
    template_name = 'accounts/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('signup')
    model = CustomUser

    def form_valid(self, form):
        context = {'form':form}
        if 'create' in self.request.POST:
            form.save()
            context['message']="登録完了しました！"
            return render(self.request,'accounts/complete.html',context)
        # elif  'back' in self.request.POST:
        #     return render(self.request,'accounts/signup.html',context)
        # elif 'create' in self.request.POST:
        #     return super().form_valid(form)
        # else:
        #     return redirect(reverse_lazy('signup'))

    # def form_invalid(self, form):
    #     context = {'form':form}
    #     context['message'] = "登録をやり直してください。"
    #     return render(self.request,'accounts/confirm.html',context)


# class ConfirmView(CreateView):
#     template_name = 'accounts/confirm.html'
#     form_class = SignupForm
#     model = CustomUser
#     # success_url = reverse_lazy('signup')

#     def form_valid(self, form):
#         context = {'form':form}
#         print(self.request.POST)
#         if self.request.POST.get('next','')=='back':
#             return render(self.request,'accounts/signup.html',context)
#         elif self.request.POST.get('next','')=='create':
#             form.save()
#             context['message'] = "登録しました！"
#         return render(self.request,'accounts/login.html', context)

#     def form_invalid(self, form):
#         context = {'form':form}
#         context['message'] = "登録をやり直してください。"
#         return redirect(to='signup')


# ログイン
class MyLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

# ログアウト
class MyLogoutView(LogoutView):
    template_name = 'accounts/logout.html'

# アカウント更新
class MyAccountView(LoginRequiredMixin,SuccessMessageMixin, UpdateView):
    template_name = 'accounts/account.html'
    model=Account
    form_class=AccountFrom

    def get_queryset(self):
        return super().get_queryset().select_related('user')

    def get_success_url(self):
        return reverse("account", kwargs={"pk":self.object.pk})

    success_message = '更新しました！'

# プロフィール更新
class MyProfileView(LoginRequiredMixin,SuccessMessageMixin, UpdateView):
    template_name = 'accounts/profile.html'
    model=Profile
    form_class=ProfileFrom

    def get_queryset(self):
        return super().get_queryset().select_related('user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image'] = Profile.objects.filter(user__username=self.request.user).values('image')
        return context

    def get_success_url(self):
        return reverse("profile", kwargs={"pk":self.object.pk})

    success_message = '更新しました！'

class MyPageView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/mypage.html'


# トップページ
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['users'] = Profile.objects.exclude(user=self.request.user).order_by('-create_date')
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.GET.get('a'):
            context['users'] = context['users'].order_by('nickname')
        elif request.GET.get('b'):
            context['users'] = context['users'].order_by('-nickname')
        elif request.GET.get('c'):
            context['users'] = context['users'].order_by('user__last_login')
        elif request.GET.get('d'):
            context['users'] = context['users'].order_by('-user__last_login')
        elif request.GET.get('e'):
            context['users'] = context['users'].order_by('create_date')
        elif request.GET.get('f'):
            context['users'] = context['users'].order_by('-create_date')
        # ページネーション
        queryset = context['users']
        page_count = 4
        context['page_obj'] = paginate_query(request,queryset,page_count)
        return render(request,self.template_name,context)

# ユーザ退会
class MyDeleteView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        return render(request,'accounts/delete.html')

    def post(self,request,*args,**kwargs):
        if 'delete' in request.POST:
            # ユーザ情報を取得
            user = CustomUser.objects.get(email=self.request.user)
            # is_activeをFalseに変更
            user.is_active = False
            user.save()
            return redirect('logout')

        elif 'cancel' in request.POST:
            # マイページに戻る
            return redirect('mypage',self.request.user.id)
        return render(request,'accounts/delete.html')

# 画像の比較ページ
class MyComparison(LoginRequiredMixin,TemplateView):
    template_name = 'accounts/comparison.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self,request,*args,**kwargs):
        context = self.get_context_data(**kwargs)
        p_user = Profile.objects.get(user__id=self.request.user.id)
        if p_user.image:
            context['others'] = akaze_comparison(self,p_user)
        else:
            context['messages'] = "画像を登録してください。"
        return render(request,self.template_name,context)

# 関数===============================================================================


# AKAZEを使ってユーザ同士の画像の類似性を比較
def akaze_comparison(self,p_user):
    # ログインユーザの画像を取得
    user = Profile.objects.values('user','nickname','image').get(user__id=self.request.user.id)
    # 他ユーザの画像を取得
    other = Profile.objects.values('user','nickname','image').exclude(user__id=self.request.user.id) \
                                                            .filter(image__istartswith='img/')
    
    # ファイル名の取得
    user_img = user['image']
    u = os.path.splitext(os.path.basename(user_img))[0]
    # ディレクトリを指定
    IMG_DIR = settings.MEDIA_ROOT
    # ファイルのフルパスを取得
    user_img_path = f"{IMG_DIR}/{user_img}"
    # 画像のリサイズ用
    IMG_SIZE = (200, 200)
    # AKAZE検出器の生成
    akz = cv2.AKAZE_create()
    # BFMatcherオブジェクトの生成
    bf = cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)
    # ログインユーザの処理
    #ターゲット画像を読み出し
    target_img = cv2.imread(user_img_path)
    # target_img = cv2.imread(user_img_path, cv2.IMREAD_GRAYSCALE)
    #ターゲット画像を200px×200pxに変換
    target_img = cv2.resize(target_img, IMG_SIZE)
    # AKAZEを適用、特徴点を検出
    target_kp, target_des = akz.detectAndCompute(target_img, None)

    other_list=[]
    # 他ユーザの処理、ログインユーザとの比較
    for f in other:
        # ファイル名の取得
        other_img = f['image']
        #ファイルのフルパスを取得
        other_img_path = f"{IMG_DIR}/{other_img}"
        try:
            #ターゲット画像を読み出し
            comparing_img = cv2.imread(other_img_path)
            # comparing_img = cv2.imread(other_img_path, cv2.IMREAD_GRAYSCALE)
            #ターゲット画像を200px×200pxに変換
            comparing_img = cv2.resize(comparing_img, IMG_SIZE)
            # AKAZEを適用、特徴点を検出
            comparing_kp, comparing_des = akz.detectAndCompute(comparing_img, None)
            # BFMatcherで総当たりマッチングを行う
            matches = bf.match(target_des, comparing_des)
            # matchesをdescriptorsの似ている順にソートする
            matches = sorted(matches, key = lambda x:x.distance)
            #特徴量の距離を出し、平均を取る
            dist = [m.distance for m in matches]
            ret = sum(dist) / len(dist)
        except:
            ret = 999999
        # 特徴量をディクショナリに追加
        f['ret'] = ret
        other_list.append(f)

    # 特徴量で並び替え(数が小さいほど似ている)
    other_list = sorted(other_list,key=lambda x:x['ret'])
    # 先頭から２つを取得
    other_list = other_list[0:3]
    for f in other_list:
        # ファイル名の取得
        other_img = f['image']
        #ファイルのフルパスを取得
        other_img_path = f"{IMG_DIR}/{other_img}"
        #ターゲット画像を読み出し
        comparing_img = cv2.imread(other_img_path)
        # comparing_img = cv2.imread(other_img_path, cv2.IMREAD_GRAYSCALE)
        #ターゲット画像を200px×200pxに変換
        comparing_img = cv2.resize(comparing_img, IMG_SIZE)
        # AKAZEを適用、特徴点を検出
        comparing_kp, comparing_des = akz.detectAndCompute(comparing_img, None)
        # BFMatcherで総当たりマッチングを行う
        matches = bf.match(target_des, comparing_des)
        # matchesをdescriptorsの似ている順にソートする
        matches = sorted(matches, key = lambda x:x.distance)
        # # 検出結果を描画する
        result = cv2.drawMatches(target_img, target_kp, comparing_img, comparing_kp, matches[0:30],None, flags = cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        #検出結果を描画した画像を出力する
        o = os.path.splitext(os.path.basename(other_img))[0]
        now = datetime.now().strftime('%Y%m%d_%H%M%S')
        # filepath = f'{IMG_DIR}/akaze/{u}_{o}_{now}.png'
        filename = f'{u}_{o}_{now}.png'
        # cv2.imwrite(filepath,result)
        # ndarrayを画像に変換
        result = result[:, :, ::-1]
        result_img = Image.fromarray(result,mode='RGB')
        image_io = io.BytesIO()
        result_img.save(image_io,format='png')
        image_file = InMemoryUploadedFile(image_io,field_name=None,name=filename,content_type="image/jpeg", size=image_io.getbuffer().nbytes,charset=None)
        cmp_user = Profile.objects.get(user=f['user'])
        # 画像を保存
        comp = ComparisonImage(
            tgt=p_user,
            cmp=cmp_user,
            ret=f['ret'],
            images=image_file,
        )
        comp.save()
    # 保存した画像をリターン
    others_list = ComparisonImage.objects.filter(tgt=p_user).order_by('create_date')[0:3]
    return others_list