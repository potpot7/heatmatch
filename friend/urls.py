from . import views
from django.urls import path

urlpatterns = [
    path('group/', views.GroupView.as_view(), name='group'),
    path('posts/', views.PostsView.as_view(), name='posts'),
    path('friends/<int:pk>', views.FriendsView.as_view(), name='friends'),
    path('message/<int:pk>/<int:name>', views.MessageView.as_view(), name='message'),
    path('message_group/<int:num>', views.MessageGroupView.as_view(), name='message_group'),
]