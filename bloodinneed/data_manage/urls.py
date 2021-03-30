from django.contrib.auth import logout
from django.urls import path
from .views import home, blog, post, login_view, signup, update, UserDetailView, logout_view, donor_list

urlpatterns = [
    path('', home, name="home"),
    path('blog', blog, name="blog"),
    path('post', post, name="post"),
    path('login', login_view, name="login"),
    path('profile/<int:pk>', UserDetailView.as_view(),name="profile"),
    path('signup', signup, name="signup"),
    path('update', update,name="update" ),
    path('logout_view/', logout_view, name='logout_view'),
    path('donor/', donor_list, name='donor'),


]