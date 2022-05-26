from django.urls import path
from . import views

app_name='home'


urlpatterns=[
    path('',views.HomeView.as_view(),name='home'),
    path('post/<int:post_id>/<slug:post_slug>/',views.PostView.as_view(),name='post'),
    path('post/delete/<int:post_id>/',views.DeleteView.as_view(),name='delete_post'),
    path('post/update/<int:post_id>/',views.UpdateView.as_view(),name='update_post'),
    path('follow/<int:user_id>/',views.FollowView.as_view(),name='follow'),
    path('unfollow/<int:user_id>/',views.UnFollowView.as_view(),name='unfollow'),
    path('reply/<int:post_id>/<int:comment_id>/',views.ReplyView.as_view(),name='reply_view'),
    path('like/<int:post_id>/',views.LikeView.as_view(),name='like_view'),
]