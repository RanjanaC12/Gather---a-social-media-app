from django.urls import path
from . import views

urlpatterns = [
    path('Users/', views.Users,name='Users'),
    path('',views.Login,name='Login'),
    path('post/',views.Add_post,name='Add_post'),
    path('friends/',views.Search_friend,name='Search_friend'),
    path('friend2/',views.Add_friend,name='Add_friend'),
    path('comments/',views.Add_comment,name='Add_comment'),
    path('likes/',views.Add_like,name='Add_like'),
    path('requests1',views.view_requests,name='view_requests'),
    path('rej_acc1/',views.accept_requests,name='accept_requests'),
    path('rej_acc2/',views.reject_request,name='reject_request'),
    path("check_friends/",views.check_friends,name='check_friends'),
    path('view_profile/',views.view_profile,name='view_profile'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('forgot.html/',views.forgot,name='forgot.html'),
    path('forgotpasswordprocess',views.forgotpasswordprocess,name='forgotpasswordprocess'),
    path('del_friend/',views.del_friend,name='del_friend'),
    ]   


