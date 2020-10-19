from django.conf.urls import url
from django.urls import include

from . import  views

urlpatterns = [
    url('signup/', views.signup, name='signup'),
    url('account/', include('django.contrib.auth.urls')),
    url('', views.index, name='index'),
    url('profile/<username>/', views.profile, name='profile'),
    url('user_profile/<username>/', views.user_profile, name='user_profile'),
    url('post/<id>', views.post_comment, name='comment'),
    url('like', views.like_post, name='like_post'),
    url('search/', views.search_profile, name='search'),
    url('follow/<to_follow>', views.follow, name='follow'),
    url('unfollow/<to_unfollow>', views.unfollow, name='unfollow'),
]