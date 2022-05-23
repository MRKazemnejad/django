from django.urls import path
from . import views

app_name='home'


urlpatterns=[
    path('',views.HomeView.as_view(),name='home'),
    path('post/<int:post_id>/<slug:post_slug>/',views.PostView.as_view(),name='post'),
    path('post/delete/<int:post_id>/',views.DeleteView.as_view(),name='delete_post'),
]