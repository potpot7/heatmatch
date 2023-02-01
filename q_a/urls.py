from . import views
from django.urls import path

urlpatterns = [
    path('question/', views.QuestionView.as_view(), name='question'),
    path('myanswer/<int:pk>', views.MyAnswerView.as_view(), name='myanswer'),
    path('otheranswer/<int:pk>', views.OtherAnswerView.as_view(), name='otheranswer'),
    path('graphcomp/<int:pk>', views.GraphComp.as_view(), name='graphcomp'),
]