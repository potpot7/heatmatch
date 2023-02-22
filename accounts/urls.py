from . import views
from django.urls import path,include
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('signup/', views.MySignupView.as_view(), name='signup'),
    path('complete/', views.MySignupView.as_view(), name='complete'),
    # path('confirm/', views.MySignupView.as_view(), name='confirm'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),
    path('account/<int:pk>/', views.MyAccountView.as_view(), name='account'),
    path('profile/<int:pk>/', views.MyProfileView.as_view(), name='profile'),
    path('mypage/<int:pk>/', views.MyPageView.as_view(), name='mypage'),
    path('', views.IndexView.as_view(), name='index'),
    path('comparison/<int:pk>/', views.MyComparison.as_view(), name='comparison'),
    path('delete/<int:pk>/', views.MyDeleteView.as_view(), name='delete'),
    path('social-auth/', include('social_django.urls', namespace='social')),
]