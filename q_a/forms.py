from django import forms
from .models import Contents,Question,Answer

class ContentsForm(forms.ModelForm):
    main_categ_choice = (
        ('趣味','趣味'),
        ('仕事','仕事'),
        ('恋愛','恋愛'),
        ('その他','その他'),
    )
    main_categ = forms.ChoiceField(choices=main_categ_choice,required=True)
    sub_categ = forms.CharField(required=True)
    contents_name = forms.CharField(required=True)

    class Meta:
        model = Contents
        fields = ['main_categ', 'sub_categ', 'contents_name']
        label = ['メインカテゴリ', 'サブカテゴリ', 'タイトル']

# class QuestionForm(forms.ModelForm):
#     q1 = forms.ChoiceField(label="",widget=forms.RadioSelect(attrs={"id":"choice1","class":"form-check-input","type":"radio"}))
#     q2 = forms.ChoiceField(label="",widget=forms.RadioSelect(attrs={"id":"choice2","class":"form-check-input","type":"radio"}))
#     q3 = forms.ChoiceField(label="",widget=forms.RadioSelect(attrs={"id":"choice3","class":"form-check-input","type":"radio"}))
#     q4 = forms.ChoiceField(label="",widget=forms.RadioSelect(attrs={"id":"choice4","class":"form-check-input","type":"radio"}))
#     q5 = forms.ChoiceField(label="",widget=forms.RadioSelect(attrs={"id":"choice5","class":"form-check-input","type":"radio"}))
#     class Meta:
#         model = Question
#         fields = ['q_title', 'q1', 'q2', 'q3', 'q4', 'q5']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['user', 'c_id', 'q_id', 'a1', 'a2', 'a3', 'a4', 'a5', 'a_val']

    def wrap_boolean_check(v):
        return not (v is False or v is None or v == '' or v == 0)