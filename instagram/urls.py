from django.urls import path, include
from . import views

urlpatterns = [
    path('accounts/register/', views.signup, name='signup'),
    path('account/',include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
    path('profile/<username>/', views.profile, name='profile'),
    path('user_profile/<username>/', views.user_profile, name='user_profile'),
    path('search/', views.search_profiles, name='search'),
    path('unfollow/<unfollowing>', views.unfollow, name='unfollow'),
    path('follow/<following>', views.follow, name='follow'),
    path('post/<id>', views.posting_comment, name='comment'),
    path('like/', views.like_post, name='like_post'),

]