from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ContentsForm, AnswerForm
# from friend.forms import FriendForm
from friend.models import Friend
from .models import Contents, Question, Answer
from accounts.models import Profile, CustomUser
from django.db.models import Q
import seaborn as sns
import plotly.offline as off
import plotly.express as px
import plotly.graph_objects as go
from django_pandas.io import read_frame


# 質問ページ
class QuestionView(LoginRequiredMixin, TemplateView):
    template_name = 'q_a/question.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # フォームの取得
        context['form'] = ContentsForm()
        # Questionのレコード取得
        context['question'] = Question.objects.all()
        return context

        # GETされたとき
    def get(self, request, *args, **kwargs):
        # get_context_dataの呼出
        context = self.get_context_data()
        return render(request, self.template_name, context)

        # POSTされたとき
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        post = request.POST
        # ラジオボタンの未選択チェック
        POST_LEN = 8  # csrf+postの数=8
        if len(post) != POST_LEN:
            context['form'] = ContentsForm(post)  # 入力された値を保持
            context['error_message'] = '未チェックの項目があります。'
            return render(request, 'q_a/question.html', context)

        # Contentsテーブルに同じものがなければ登録
        contents = ContentsForm(request.POST, instance=Contents())
        if contents.is_valid():
            if Contents.objects.filter(main_categ=request.POST['main_categ'],
                                       sub_categ=request.POST['sub_categ'],
                                       contents_name=request.POST['contents_name']
                                       ).exists() == False:
                contents.save()

        # Answerテーブルへの登録
        # ユーザを取得
        u = request.user
        # c_idを取得
        c = Contents.objects.get(main_categ=request.POST['main_categ'],
                                 sub_categ=request.POST['sub_categ'],
                                 contents_name=request.POST['contents_name'])
        # Questionテーブルを取得
        q_list = context['question']
        # boolean登録用
        A_NUM = 1
        # POSTされたアイテムを取出
        for key, i in post.items():
            # Questionテーブルから取出
            for q in q_list:
                q_id = q.q_id
                # 質問と回答を紐づけ
                if str(key) == str(q_id):
                    # ラジオボタンでの回答の値を数値で取得
                    a_val = int(i)
                    # 回答の値によってラジオボタンの結果を保存
                    if 1 <= a_val <= 4:
                        answer = Answer(user=u, c_id=c, q_id=q,
                                        a1=A_NUM, a_val=a_val)
                    elif 5 <= a_val <= 9:
                        answer = Answer(user=u, c_id=c, q_id=q,
                                        a2=A_NUM, a_val=a_val)
                    elif 10 <= a_val <= 14:
                        answer = Answer(user=u, c_id=c, q_id=q,
                                        a3=A_NUM, a_val=a_val)
                    elif 15 <= a_val <= 19:
                        answer = Answer(user=u, c_id=c, q_id=q,
                                        a4=A_NUM, a_val=a_val)
                    elif 20 <= a_val <= 30:
                        answer = Answer(user=u, c_id=c, q_id=q,
                                        a5=A_NUM, a_val=a_val)
                    answer.save()
                    context['success_message'] = '登録しました！'

        return render(request, self.template_name, context)


# 自分の回答ページ
class MyAnswerView(LoginRequiredMixin, TemplateView):
    template_name = 'q_a/myanswer.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['user'] = Profile.objects.get(user=request.user)
        # Answerテーブルにログインユーザのデータの存在チェック
        if Answer.objects.filter(user=request.user).exists():
            context['plot_fig'] = graph_conv(request.user)
            # ログインユーザの回答履歴を取得
            context['answer_result'] = Answer.objects.select_related('c_id').select_related(
                'q_id').filter(user=request.user).order_by("create_date").reverse()
            # ページネーション
            queryset = context['answer_result']
            page_count = 16
            context['page_obj'] = paginate_query(request,queryset,page_count)
        else:
            context['no_answer'] = "まだ回答履歴がありません。"

        return render(request, self.template_name, context)


# 他の人の回答ページ
class OtherAnswerView(LoginRequiredMixin, TemplateView):
    template_name = 'q_a/otheranswer.html'

    # 共通処理
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 他の人のプロフィール情報を取得
        pk = self.kwargs['pk']
        context['user'] = Profile.objects.select_related('user').get(user_id=pk)
        # Answerテーブルにユーザのデータの存在チェック
        if Answer.objects.filter(user=context['user'].user).exists():
            context['plot_fig'] = graph_conv(context['user'].user)
        else:
            context['no_answer'] = "まだ回答履歴がありません。"
        return context

    # GETのとき
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    # POSTのとき
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        user = Profile.objects.get(user=request.user)
        if 'follow' in request.POST:
            follow = Friend.objects.get_or_create(follower=user,
                                             followed=context['user'])
            if follow[1] == True:
                context['fol_messages'] ="フォローしました！"
            else:
                context['fol_messages'] ="すでにフォローしています"
        if 'delete' in request.POST:
            try:
                follow = Friend.objects.get(follower=user,
                                        followed=context['user']).delete()
                context['del_messages'] ="もうフォロー解除しました。"
            except Friend.DoesNotExist:
                context['del_messages'] ="フォローしていません。"

        return render(request, self.template_name, context)

# 回答の比較ページ
class GraphComp(LoginRequiredMixin,TemplateView):
    template_name = 'q_a/graphcomp.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if Answer.objects.filter(user=self.request.user).exists():
            context['my_plot'] = graph_conv(self.request.user)
        else:
            context['my_plot'] = "まだ回答がありません。"
        context['me'] = Profile.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        # 自分の回答情報を取得
        if Answer.objects.filter(user=self.request.user).exists():
            my_ans = Answer.objects.filter(user=self.request.user).order_by('?')
            my_ans = list(my_ans)
            # 自分と似ている回答をしたユーザがいるか判定
            u = ""
            for m in my_ans:
                if Answer.objects.filter(c_id=m.c_id).exclude(user=self.request.user).exists():
                    u = Answer.objects.filter(c_id=m.c_id).exclude(user=self.request.user).first()
                    context['title'] = "同じコンテンツの回答をしたユーザ"
                    break
            if u == "":
                for m in my_ans:
                    if Answer.objects.filter(c_id__sub_categ=m.c_id.sub_categ,c_id__contents_name=m.c_id.contents_name).exclude(user=self.request.user).exists():
                        u = Answer.objects.filter(c_id__sub_categ=m.c_id.sub_categ,c_id__contents_name=m.c_id.contents_name).exclude(user=self.request.user).first()
                        context['title'] = "同じサブカテゴリ、同じタイトルの回答をしたユーザ"
                        break
            if u == "":
                for m in my_ans:
                    if Answer.objects.filter(c_id__contents_name=m.c_id.contents_name).exclude(user=self.request.user).exists():
                        u = Answer.objects.filter(c_id__contents_name=m.c_id.contents_name).exclude(user=self.request.user).first()
                        context['title'] = "同じタイトルの回答をしたユーザ"
                        break
            if u == "":
                for m in my_ans:
                    if Answer.objects.filter(c_id__sub_categ=m.c_id.sub_categ).exclude(user=self.request.user).exists():
                        u = Answer.objects.filter(c_id__sub_categ=m.c_id.sub_categ).exclude(user=self.request.user).first()
                        context['title'] = "同じサブカテゴリの回答をしたユーザ"
                        break
                    else:
                        context['title'] = "もっと回答をしてみてください。"
            context['your_plot'] = graph_conv(u.user)
            context['you'] = Profile.objects.get(user=u.user)
        else:
            pass
        return render(request, self.template_name, context)

# 関数===============================================================================


# 回答結果をグラフ化
def graph_conv(user):
    # 回答情報を取得
    ans_res = Answer.objects.filter(user=user).select_related('c_id')
    # DateFrame型に変換
    df = read_frame(ans_res, fieldnames=[
                    'user__id', 'c_id__main_categ', 'c_id__sub_categ', 'c_id__contents_name', 'a_val'])
    fig = px.treemap(df, path=[px.Constant("HeatMap"), 'c_id__main_categ', 'c_id__sub_categ', 'c_id__contents_name'],
                     values='a_val')
    fig.update_traces(root_color="lightgrey")
    plot_fig = off.plot(fig, output_type='div', include_plotlyjs=False)
    return plot_fig

# ページネーション
def paginate_query(request, queryset, count):
  paginator = Paginator(queryset, count)
  page = request.GET.get('page')
  try:
    page_obj = paginator.page(page)
  except PageNotAnInteger:
    page_obj = paginator.page(1)
  except EmptyPage:
    page_obj = paginator.page(paginator.num_pages)
  return page_obj