
from django.contrib import admin
from django.urls import path
from . import views
from .controllers import user_view

urlpatterns = [
    path('', user_view.index_page ,name='index_page'),
    path('video', user_view.video_page ,name='video_page'),
    path('video/detail', user_view.video_detail_page ,name='video_detail_page'),
    

     
]

